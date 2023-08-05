import numpy as np
from keras.models import Model
from keras.layers import Dense, Input, Lambda, Concatenate, Reshape
from keras import backend as K
from pylation.mlp import MLP


class relational():
    '''
    Create a fully connected Relational Network that can be used as if it were
    a keras layer. The user specifies the hyperparameters for each of the
    stacked MLP networks.

    '''

    def __init__(self, ORin, OSin, hyperparams1, hyperparams2):
        '''
        Initialize the Relational Network (RN)

        # Arguments
        -----------
        Oin: keras tensor
            Symbolic tensor of shape (batch_size, N_objects, N_variables)
            where N_objects is the number of different unique objects to relate
            each of which will be described by N_variables
        hyperparams1: dict
            Hyperparameters for the first MLP in the RN
        hyperparams2: dict
            Hyperparameters for the second MLP in the RN

            hyperparams1 & 2 to be specified by user:
                # Arguments
                ------------
                    N_layers : int
                        Depth of the MLP.
                    activations : list
                        List of activation functions for each layer, in order
                        from first to last.
                    layer_size : list
                        Layers sizes in order from first to last.
                    dropout : bool, optional
                        If set to True, dropout of 20% will be used
                        The default is True

                        If set to False, dropout will not be used
                    L1 : float
                        L1 weight regularization factor
                        Default is 0.0 or no L1
                    L2 : float
                        L2 weight regularization factor
                        Default is 0.0 or no L2
        '''

        self.ORin = ORin
        self.OSin = OSin
        self.Sdims = self.OSin.shape
        self.Rdims = self.ORin.shape
        self.hyperparams1 = hyperparams1
        self.hyperparams2 = hyperparams2

    def make_Rs_Rr(self, n, m):
        '''
        Create the necessary relational matrices of shape n x n.
        Where n is the number of unique objects (magnetometer stations etc)
        There are two relational matrices: "Sender" (Rs) and "Receiver" (Rr)

        # Example
        ---------
        >>> n = 3
        >>> Rr, Rs = make_Rs_Rr(n)
         Rr:                      Rs:
        |1 1 1 0 0 0 0 0 0|      |1 0 0 1 0 0 1 0 0|
        |0 0 0 1 1 1 0 0 0|      |0 1 0 0 1 0 0 1 0|
        |0 0 0 0 0 0 1 1 1|      |0 0 1 0 0 1 0 0 1|
        '''
        Rr = np.identity(n)
        Rr = np.repeat(Rr, m, axis=1)
        Rs = np.identity(m).reshape(1, m, m)
        Rs = np.repeat(Rs, n, axis=0)
        Rs = Rs.reshape(n*m, m).T
        return Rr, Rs

    def permutate(self, data_Rin, data_Sin):
        '''
        Create all possible combinations of object-object relationships by
        populating an untrainable Keras model with the proper matrices.

        # Example
        ------------
        Let A, B, C be a set of unique objects with 4 variables per object
        Input Set:
            [A1 A2 A3 A4] == [A]
            [B1 B2 B3 B4] == [B]
            [C1 C2 C3 C4] == [C]

            Output:                           Relations:
                [A1 A2 A3 A4 A1 A2 A3 A4]     ----> A:A relation
                [A1 A2 A3 A4 B1 B2 B3 B4]     ----> A:B relation
                [A1 A2 A3 A4 C1 C2 C3 C4]     ----> A:C relation
                [B1 B2 B3 B4 A1 A2 A3 A4]     ----> B:A relation
                [B1 B2 B3 B4 B1 B2 B3 B4]     ----> B:B relation
                [B1 B2 B3 B4 C1 C2 C3 C4]     ----> B:C relation
                [C1 C2 C3 C4 A1 A2 A3 A4]     ----> C:A relation
                [C1 C2 C3 C4 B1 B2 B3 B4]     ----> C:B relation
                [C1 C2 C3 C4 C1 C2 C3 C4]     ----> C:C relation


        More explicitly:

          Input of
          function
             |
             V
                                       STEP 1
                                      --------
                       Input Dot Rr
                            Rr:                     "receiver"
            [A]     |1 1 1 0 0 0 0 0 0|
            [B] Dot |0 0 0 1 1 1 0 0 0| = [[A] [A] [A] [B] [B] [B] [C] [C] [C]]
            [C]     |0 0 0 0 0 0 1 1 1|


                                       STEP 2
                                      --------

                       Input dot Rs
                            Rs:                      "sender"
            [A]     |1 0 0 1 0 0 1 0 0|
            [B] Dot |0 1 0 0 1 0 0 1 0| = [[A] [B] [C] [A] [B] [C] [A] [B] [C]]
            [C]     |0 0 1 0 0 1 0 0 1|


                                      STEP 3
                                     ---------

             Concatenate "receiver" and "sender":     [[A A]
                                                       [A B]
                                                       [A C]
             [[A] [A] [A] [B] [B] [B] [C] [C] [C]] or  [B A]
               v   v   v   v   v   v   v   v   v  ===> [B B]
             [[A] [B] [C] [A] [B] [C] [A] [B] [C]]     [B C]
                                                       [C A]
                                                       [C B]
                                                       [C C]]

        '''

        def transpose_3tensor(t):
            '''
            Lambda function to switch dimensions of input in order to properly
            take the dot product and return the necessary relationships
            '''
            return K.permute_dimensions(t, (0, 2, 1))

        Rr, Rs = self.make_Rs_Rr(int(self.Rdims[1]), int(self.Sdims[1]))
        self.receiver = Rr
        self.sender = Rs

        Sin = Input((self.Sdims[1:]))
        Rin = Input((self.Rdims[1:]))

        self.Rr = Dense(int(self.Sdims[1]*self.Rdims[1]), use_bias=False)
        self.Rr.trainable = False
        self.Rs = Dense(int(self.Sdims[1]*self.Rdims[1]), use_bias=False)
        self.Rs.trainable = False

        T = Lambda(transpose_3tensor)
        ORin = Rin
        OSin = Sin
        OR = T(ORin)
        OS = T(OSin)
        r = self.Rr(OR)
        r = T(r)
        s = self.Rs(OS)
        s = T(s)
        out = Concatenate(axis=-1)([r, s])
        relations = Model(inputs=[Rin, Sin], outputs=out)
        relations.set_weights([self.receiver, self.sender])
        return relations([data_Rin, data_Sin])

    def recombine(self, t):

        '''
        Upon feeding the output of permutate() through an MLP in a row-wise
        fashion, the results are recombined by summing the variables to create
        a generalized relation for each input object.

        # Example
        ---------                      Input of this
                                         function
                                             |
                                             V

               1              2              3                     4

                                    |Each output is   |
        |Input each into same MLP|  |an unknown vector|          |Sum|
        --------------------------   -----------------    --------------------
        [A1 A2 ... A3 A4] -> MLP -> [AA1 AA2 ... AAN] \
        [A1 A2 ... B3 B4] -> MLP -> [AB1 AB2 ... ABN] |-> [ABC1 ABC2 ... ABCN]
        [A1 A2 ... C3 C4] -> MLP -> [AA1 AA2 ... ACN] /
        [B1 B2 ... A3 A4] -> MLP -> [AA1 AA2 ... BAN] \
        [B1 B2 ... B3 B4] -> MLP -> [AA1 AA2 ... BBN] |-> [BAC1 BAC2 ... BACN]
        [B1 B2 ... C3 C4] -> MLP -> [AA1 AA2 ... BCN] /
        [C1 C2 ... A3 A4] -> MLP -> [AA1 AA2 ... CAN] \
        [C1 C2 ... B3 B4] -> MLP -> [AA1 AA2 ... CBN] |-> [CAB1 CAB2 ... CABN]
        [C1 C2 ... C3 C4] -> MLP -> [AA1 AA2 ... CCN] /
                                                                  |
                                                                  |
                                                                  |
                       ___________________________________________|
                       |
                       |
                       V

                       5

         |Concatenate original Objects|
        --v--v--v--v--------------------
       [[A1 A2 A3 A4 ABC1 ABC2 ... ABCN]
        [B1 B2 B3 B4 BAC1 BAC2 ... BACN]
        [C1 C2 C3 C4 CAB1 CAB2 ... CABN]]
                       |
                       |
                       V
                    Output


        '''
        def sums(t):
            '''
            Simple Keras lambda function to sum along inner axis
            '''
            return K.sum(t, axis=-2)
        Sum = Lambda(sums)
        out = Reshape((int(self.Rdims[1]),
                       int(self.Sdims[1]),
                       int(t.shape[-1])))(t)

        out = Sum(out)
#        out = Flatten()(out)
        out = Concatenate(axis=-1)([self.ORin, out])

        return out

    def Run(self):
        '''
        Initiate two MLPs within this Relational Network using the supplied
        hyperparameters for each of the two MLPs
        '''
        F_in = self.permutate(self.ORin, self.OSin)
        Fout = MLP(F_in, **self.hyperparams1)
        E = self.recombine(Fout)
        Gout = MLP(E, **self.hyperparams2)
        return Gout


def Relational(ORin, OSin, hyperparams1, hyperparams2):
    return relational(ORin, OSin, hyperparams1, hyperparams2).Run()

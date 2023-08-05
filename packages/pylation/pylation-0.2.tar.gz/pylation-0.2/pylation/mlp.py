from keras.layers import Dense, Dropout, TimeDistributed
from keras.regularizers import L1L2


class mlp:
    ''' Given a set of hyperparameters:
        + Create an MLP model of proper shape and dimension
        + Feed the data through this MLP
    '''

    def __init__(self,

                 N_layers,
                 activations,
                 layer_size,
                 dropout=True,
                 L1=0.0,
                 L2=0.0,
                 timedistributed=True):
        ''' Initialize the hyperparameters and build the MLP.

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
        self.layers = N_layers
        self.activations = activations
        self.sizes = layer_size
        self.dropout = dropout
        self.L1 = L1
        self.L2 = L2
        self.timedistributed = timedistributed
        self.module = self.build_module()

    def build_module(self):
        '''
        Build the module from the initialized arguments above

        # Returns
        ---------
            collection: list
                list of layers according to the specified hyperparameters
        '''
        collection = []
        if self.timedistributed:
            for i in range(self.layers):
                tmp = TimeDistributed(Dense(self.sizes[i]))
                activation = self.activations[i]
                collection.append(tmp)
                collection.append(activation)

                if self.dropout:
                    tmp = Dropout(0.25)
                    collection.append(tmp)
                if (self.L1 + self.L2) > 0.0:
                    tmp = L1L2(self.L1, self.L2)
                    collection.append(tmp)
        else:
            for i in range(self.layers):
                tmp = Dense(self.sizes[i], activation=self.activations[i])
                collection.append(tmp)
                if self.dropout:
                    tmp = Dropout(0.3)
                    collection.append(tmp)
                if (self.L1 + self.L2) > 0.0:
                    tmp = L1L2(self.L1, self.L2)
                    collection.append(tmp)

        return collection

    def Out(self, data):
        ''' Feed data through each layer of the MLP

        # Arguments
        -----------
            data: keras tensor
                tensor of the input data for the MLP

        # Returns
        ----------
            data: keras tensor
                tensor of the MLP's output
        '''
        for layer in self.module:
            data = layer(data)
        return data


def MLP(data, **hyperparams):
    return mlp(**hyperparams).Out(data)

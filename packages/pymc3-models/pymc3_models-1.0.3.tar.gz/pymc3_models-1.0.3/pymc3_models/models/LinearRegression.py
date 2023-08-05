import numpy as np
import pymc3 as pm
from sklearn.metrics import r2_score
import theano
import theano.tensor as T

from pymc3_models.exc import PyMC3ModelsError
from pymc3_models.models import BayesianModel


class LinearRegression(BayesianModel):
    """
    Linear Regression built using PyMC3.
    """

    def __init__(self):
        super(LinearRegression, self).__init__()

    def create_model(self):
        """
        Creates and returns the PyMC3 model.

        Note: The size of the shared variables must match the size of the training data. Otherwise, setting the shared variables later will raise an error. See http://docs.pymc.io/advanced_theano.html

        Returns
        ----------
        the PyMC3 model
        """
        model_input = theano.shared(np.zeros([self.num_training_samples, self.num_pred]))

        model_output = theano.shared(np.zeros(self.num_training_samples))

        self.shared_vars = {
            'model_input': model_input,
            'model_output': model_output,
        }

        model = pm.Model()

        with model:
            alpha = pm.Normal('alpha', mu=0, sd=100, shape=(1))
            betas = pm.Normal('betas', mu=0, sd=100, shape=(1, self.num_pred))

            s = pm.HalfNormal('s', tau=1)

            mean = alpha + T.sum(betas * model_input, 1)

            y = pm.Normal('y', mu=mean, sd=s, observed=model_output)

        return model

    def fit(self, X, y, inference_type='advi', minibatch_size=None, inference_args=None):
        """
        Train the Linear Regression model

        Parameters
        ----------
        X : numpy array, shape [n_samples, n_features]

        y : numpy array, shape [n_samples, ]

        inference_type : string, specifies which inference method to call. Defaults to 'advi'. Currently, only 'advi' and 'nuts' are supported

        minibatch_size : number of samples to include in each minibatch for ADVI, defaults to None, so minibatch is not run by default

        inference_args : dict, arguments to be passed to the inference methods. Check the PyMC3 docs for permissable values. If no arguments are specified, default values will be set.
        """
        self.num_training_samples, self.num_pred = X.shape

        self.inference_type = inference_type

        if y.ndim != 1:
            y = np.squeeze(y)

        if not inference_args:
            inference_args = self._set_default_inference_args()

        if self.cached_model is None:
            self.cached_model = self.create_model()

        if minibatch_size:
            with self.cached_model:
                minibatches = {
                    self.shared_vars['model_input']: pm.Minibatch(X, batch_size=minibatch_size),
                    self.shared_vars['model_output']: pm.Minibatch(y, batch_size=minibatch_size),
                }

                inference_args['more_replacements'] = minibatches
        else:
            self._set_shared_vars({'model_input': X, 'model_output': y})

        self._inference(inference_type, inference_args)

        return self

    def predict(self, X, return_std=False):
        """
        Predicts values of new data with a trained Linear Regression model

        Parameters
        ----------
        X : numpy array, shape [n_samples, n_features]

        return_std : Boolean flag of whether to return standard deviations with mean values. Defaults to False.
        """

        if self.trace is None:
            raise PyMC3ModelsError('Run fit on the model before predict.')

        num_samples = X.shape[0]

        if self.cached_model is None:
            self.cached_model = self.create_model()

        self._set_shared_vars({'model_input': X, 'model_output': np.zeros(num_samples)})

        ppc = pm.sample_ppc(self.trace, model=self.cached_model, samples=2000)

        if return_std:
            return ppc['y'].mean(axis=0), ppc['y'].std(axis=0)
        else:
            return ppc['y'].mean(axis=0)

    def score(self, X, y):
        """
        Scores new data with a trained model.

        Parameters
        ----------
        X : numpy array, shape [n_samples, n_features]

        y : numpy array, shape [n_samples, ]
        """

        return r2_score(y, self.predict(X))

    def save(self, file_prefix):
        params = {
            'inference_type': self.inference_type,
            'num_pred': self.num_pred,
            'num_training_samples': self.num_training_samples
        }

        super(LinearRegression, self).save(file_prefix, params)

    def load(self, file_prefix):
        params = super(LinearRegression, self).load(file_prefix, load_custom_params=True)

        self.inference_type = params['inference_type']
        self.num_pred = params['num_pred']
        self.num_training_samples = params['num_training_samples']

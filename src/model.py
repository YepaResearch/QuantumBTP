from hmmlearn import hmm


def init_hmm(_states=4, _iter=100):
    """
    
    Initialize a Gaussian Hidden Markov Model.
    
    Args:
    _states (int) (defval=4  ): Number Of States
    _iter   (int) (defval=100): Number Of Iteration

    Returns:
    _model (Model): Initialized Hidden Markov Model
    
    """
    _model = hmm.GaussianHMM(n_components=_states, covariance_type="diag", n_iter=_iter)
    return _model

def train_hmm(_model, _x):
    """
    
    Train the HMM on the provided data.
    
    Args:
    _model (Model)    : Hidden Markov Model
    _X     (Dataframe): Dataframe with Model Training Matrix

    Returns:
    _model (Model): Trained Hidden Markov Model
    """
    _model.fit(_x)
    return _model

def predict_states(_model, _x):
    """
    Predict states using the trained HMM.
    
    Args:
    _model (Model)    : Hidden Markov Model
    _X     (Dataframe): Dataframe with Model Training Matrix

    Returns:
    _states (DataFrame): DataFrame with Predictions from Hidden Markov Model
    """
    _states = _model.predict(_x)
    return _states

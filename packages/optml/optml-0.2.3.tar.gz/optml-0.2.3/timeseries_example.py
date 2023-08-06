import numpy as np
import matplotlib.pyplot as plt

import statsmodels.api as sm

from random_search import RandomSearchOptimizer
from bayesian_optimizer import BayesianOptimizer
from genetic_optimizer import GeneticOptimizer
from optimizer_base import Parameter

if __name__ == "__main__":
    nile_data = np.array([x[1] for x in sm.datasets.nile.load().data])

    from statsmodels.tsa.statespace.sarimax import SARIMAX
    sarimax = SARIMAX(endog=nile_data)

    sarimax_params = [Parameter(name='order', param_type='int_array', lower=[1, 0, 0], upper=[3, 3, 3]),
                      Parameter(name='seasonal_order', param_type='int_array', lower=[0, 0, 0, 0], upper=[2, 2, 2, 12])]

    def mse(y_true,y_pred):
        return np.sqrt(1./len(y_true) * np.sum((y_true-y_pred)**2))

    rand_search = RandomSearchOptimizer(model=sarimax,
                                        eval_func=mse,
                                        hyperparams=sarimax_params,
                                        grid_size=10)

    rand_best_params, rand_best_model = rand_search.fit(nile_data, nile_data, n_iters=50)
    import sys; sys.exit()

    kernel = gp.kernels.Matern()        
    bayesOpt = BayesianOptimizer(model=sarimax, 
                                 hyperparams=sarimax_params, 
                                 kernel=kernel,                                  
                                 eval_func=mse)
    


    n_init_samples = 4    
    #mutation_noise = {'hidden_dim': 5}
    mutation_noise = {'C': 0.4, 'degree': 0.4}    
    svm_bounds = {'C':[0.1,5],'degree':[1,5]}    

    geneticOpt = GeneticOptimizer(svm, svm_params, clf_score, n_init_samples, 
                                 'RouletteWheel', mutation_noise)
    genetic_best_params, genetic_best_model = geneticOpt.fit(X_train, y_train, X_test, y_test, 50)    

    rand_best_params, rand_best_model = rand_search.fit(X_train, y_train, X_test, y_test, 50)
    bayes_best_params, bayes_best_model = bayesOpt.fit(X_train, y_train, X_test, y_test, 10)
    genetic_best_params, genetic_best_model = geneticOpt.fit(X_train, y_train, X_test, y_test, 50)    

    rand_best_model.fit(data, target)
    print("Random Search: {}".format(clf_score(y_test, rand_best_model.predict(X_test))))

    bayes_best_model.fit(data, target)
    print("Bayesian Optimisation: {}".format(clf_score(y_test, bayes_best_model.predict(X_test))))

    genetic_best_model.fit(data, target)    
    print("Genetic Algo: {}".format(clf_score(y_test, genetic_best_model.predict(X_test))))

    plt.plot([v[0] for v in bayesOpt.hyperparam_history], label='BayesOpt')
    plt.plot([v[0] for v in rand_search.hyperparam_history], label='Random Search')
    plt.plot([v[0] for v in geneticOpt.hyperparam_history], label='Genetic Algo')    
    plt.legend()
    plt.show()

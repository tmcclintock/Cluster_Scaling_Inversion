"""
Implement the actual inversion.
"""
import beta_implementations as betas

#Notes to myself: actual inputs to the conversion are an array of normalizations and slopes of the relevant scaling laws (pis and alphas) as well as a covariance matrix describing their relation, as well as pivot values for everything.

class Inversion(object):

    def __init__(self):
        self.beta_function = betas.get_cosmocalc_beta

    def select_beta_function(self, choice):
        if choice == 0:
            self.beta_function = betas.get_CCL_beta
        elif choice == 1:
            self.beta_function = betas.get_aemulus_beta
        elif choice == 2:
            self.beta_function = betas.get_cosmocalc_beta
        else:
            raise Exception("Beta function choice must be 0, 1, or 2.")
        return

    def setup_inversion(self, pivots, alphas, cov):
        self.pivots = pivots
        self.alphas = alphas
        self.cov = cov


if __name__ == "__main__":
    inv = Inversion()
    inv.select_beta_function(0)
    inv.select_beta_function(1)
    inv.select_beta_function(2)
    try:
        inv.select_beta_function(3)
    except Exception:
        print "Beta function selection exception correctly raised."

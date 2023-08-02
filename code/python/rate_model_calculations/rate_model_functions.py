import sys
import pathlib
import numpy as np
import rate_model_coeffs
import matplotlib.pyplot as plt

utils_path = pathlib.Path(__file__).parent.parent.joinpath("utils").as_posix()
sys.path.append(utils_path)

from distance_utils import frequency_approx, averaged_distance



def l(x):
    return 0.91149071*x -0.01253742

#distance from above line
def dl(x1,y1):
    return -(0.91149071 * x1 -1 * y1 -0.01253742) / (np.sqrt((0.91149071 * 0.91149071) + 1))

class RateModelFunctions:
    def __init__(self, d_biff_coeff = [], 
                 freq_app_coeff = [], 
                 currents_values = []):
        self.d_biff_coeff = d_biff_coeff
        self.freq_app_coeff = freq_app_coeff
        self.current_values = currents_values
        self.__d_biff_func = lambda x,a,b,c: a*(x**2) + b*x + c
        self.__freq_func = lambda x,a,b: a*np.sqrt(x) + b*x
        self.averaged_freq_func_coeffs = ()
        self.averaged_d_biff_func_coeffs = ()


    def d_biff_iapp(self, index, x):
        assert index < len(self.d_biff_coeff)
        return self.__d_biff_func(x,
                                  self.d_biff_coeff[index][0],
                                  self.d_biff_coeff[index][1],
                                  self.d_biff_coeff[index][2])
    
    def averaged_d_biff(self, x):
        assert len(self.averaged_d_biff_func_coeffs) >= 3
        return self.__d_biff_func(x,
                                  self.averaged_d_biff_func_coeffs[0],
                                  self.averaged_d_biff_func_coeffs[1],
                                  self.averaged_d_biff_func_coeffs[2])


    
    def print_d_biff_iapp(self, index, x):
        print(r'%f*(%f**2) + %f*%f + %f' % (self.d_biff_coeff[index][0],
                                         x,
                                         self.d_biff_coeff[index][1],
                                         x,
                                         self.d_biff_coeff[index][2]))
    
    def freq_iapp(self, index, z, d):
        assert index < len(self.freq_app_coeff)
        return self.__freq_func(d-self.d_biff_iapp(index,z),
                                self.freq_app_coeff[index][0],
                                self.freq_app_coeff[index][1])
    
    def averaged_freq(self, z, d):
        assert len(self.averaged_freq_func_coeffs) >= 2
        return self.__freq_func(d-self.averaged_d_biff(z),
                                self.averaged_freq_func_coeffs[0],
                                self.averaged_freq_func_coeffs[1])
    
    def print_freq_iapp(self, index, z, d):
        print(r'%f*np.sqrt(%f) + %f*%f'%(
            self.freq_app_coeff[index][0],
             d-self.d_biff_iapp(index,z),
             self.freq_app_coeff[index][1],
             d-self.d_biff_iapp(index,z)))
    
    def M_iapp(self, index, z, d):
        if d >= self.d_biff_iapp(index,z):
            return self.freq_iapp(index, z, d)
        return(0)
    
    def add_to_list(self, a, l):
        l.append(a)

    def averaged_freq_values(self, z, d):
        sum = 0
        for i in range(len(self.freq_app_coeff)):
            sum += self.freq_iapp(i, z, d)       
        return sum/len(self.freq_app_coeff)
    
    def averaged_d_biff_values(self, z):
        sum = 0
        for i in range(len(self.d_biff_coeff)):
            sum += self.d_biff_iapp(i, z)       
        return sum/len(self.d_biff_coeff)

    def calculate_averaged_func_coeffs(self, z):
        x = np.linspace(0.1,1)
        y = self.averaged_freq_values(z,x)
        popt = frequency_approx(x,y,self.__freq_func)
        self.averaged_freq_func_coeffs = popt
        return popt

    def calculate_averaged_d_biff_coeffs(self):
        x = np.linspace(0.1,1)
        y = self.averaged_d_biff_values(x)
        popt = frequency_approx(x,y,self.__d_biff_func)
        self.averaged_d_biff_func_coeffs = popt
        return popt

    def average_distance_freq(self, ind1, ind2, zval):
        assert ind1 < len(self.freq_app_coeff)
        assert ind2 < len(self.freq_app_coeff)
        x = np.linspace(0.1, 1)
        y1 = self.freq_iapp(ind1, zval, x)
        y2 = self.freq_iapp(ind2, zval, x)
        return averaged_distance(x, y1, x, y2)

    def plot_freq_equations(self, zval):
        legend = []
        d = np.linspace(0, 1)

        for i in range(len(self.current_values)):
            legend.append(r'iApp = %dmA' % (self.current_values[i]))
        #legend.append('averaged freq values')
        #legend.append('aveeraged freq equation')
        plt.figure()
        for i in range(len(self.freq_app_coeff)):
            plt.plot(d, self.freq_iapp(i, zval, d))

        #plt.plot(d, self.averaged_freq_values(zval,d))
        #plt.plot(d, self.averaged_freq(zval,d))




        plt.title('frequency vs d')

        plt.legend(legend)

        plt.xlabel('d')
        plt.ylabel('val on line')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.show()

    def plot_saddel_point_equations(self, maxx=0.23, maxy=0.27):
        legend = []
        d = np.linspace(0, 1)

        for i in range(len(self.current_values)):
            legend.append(r'iApp = %dmA' % (self.current_values[i]))
        plt.figure()
        for i in range(len(self.d_biff_coeff)):
            plt.plot(d, self.d_biff_iapp(i, d))

        plt.title('d vs z')

        plt.legend(legend)

        plt.xlabel('d')
        plt.ylabel('z')
        plt.xlim(0, maxx)
        plt.ylim(0, maxy)
        plt.show()


                                 


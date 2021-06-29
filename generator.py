# -*- coding: utf-8 -*-
from math import pi, sin
import numpy as np
import matplotlib.pyplot as plt
import random
import copy
# import logging
# logging.basicConfig(level=logging.DEBUG)
# # logging.basicConfig(level=logging.CRITICAL)
# logger = logging.getLogger('main')
from observer import *
from utils import degree_radian


class Generator(Subject):
    def __init__(self, name="signal", mag=1.0, freq=1.0, phase=0.0, harm=1, color="black"):
        Subject.__init__(self)
        self.name = name
        self.mag, self.freq, self.phase, self.harmonics = mag, freq, phase, harm
        self.samples = 1000
        self.steps = 5
        self.harmo_odd_even = 1
        self.signal = []
        self.signals = {}
        self.color = color

    def __repr__(self):
        return "<Generator(mag:{}, freq:{}, phase:{})>".format(self.mag, self.freq, self.phase)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_signal(self):
        # signal=copy.copy(self.signal)
        return self.signal

    def get_signals(self):
        # signal=copy.copy(self.signal)
        return self.signals

    def get_magnitude(self):
        return self.mag

    def set_magnitude(self, mag):
        self.mag = mag

    def get_frequency(self):
        return self.freq

    def set_frequency(self, freq):
        self.freq = freq

    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase

    def get_samples(self):
        return self.samples

    def set_samples(self, samples):
        self.samples = samples

    def get_steps(self):
        return steps

    def set_steps(self, steps):
        self.steps = steps

    def get_harmonics(self):
        return self.harmonics

    def set_harmonics(self, harmonics):
        self.harmonics = harmonics

    def vibration(self, t):
        a, f, p, harmonics = self.mag, self.freq, self.phase, self.harmonics
        radians = degree_radian(p)
        sum = a*sin(2*pi*f*t)-radians
        for h in range(2, harmonics+1):
            if self.harmo_odd_even == 1:
                sum = sum+(a*1.0/h)*sin(2*pi*(f*h)*t-radians)
            elif self.harmo_odd_even == 2 and h % 2 == 1:
                sum = sum+(a*1.0/h)*sin(2*pi*(f*h)*t-radians)
        return sum

    def generate(self, period=2):
        del self.signal[0:]
        echantillons = range(int(self.samples)+1)
        Tech = period/self.samples
        for t in echantillons:
            self.signal.append([t*Tech, self.vibration(t*Tech)])
        self.notify()
        return self.signal

    def delete(self):
        del self.signal[0:]
        self.notify()

class Lissajou(Subject) :
    def __init__(self,name,signal1,signal2,color="red"):
        Subject.__init__(self)
        self.name = name
        self.signal=[]
        self.color=color
        self.signal1,self.signal2=signal1,signal2
        self.generate_signal()
        
    def generate_signal(self):
        del self.signal[0:]
        samples=1000
        i=0
        for i in range(0, len(self.signal1)):
                self.signal.append((self.signal1[i][1], self.signal2[i][1]))
        self.notify()

    


class PreyPredator(Subject):
    def __init__(self, alpha=0.8, beta=0.4, gamma=0.6, delta=0.2, preys=3, predators=5):
        Subject.__init__(self)
        self.a, self.b, self.g, self.d = alpha, beta, gamma, delta
        # self.a,self.b,self.g,self.d=1.5,0.05,0.48,0.05
        self.x, self.y = preys, predators
        self.population = []
        self.start, self.stop = 0.0, 100.0
        self.samples = 1000

    def preys_evolution(self, x, y):
        """
        x: preys
        y: predators
        """
        return x*(self.a-self.b*y)

    def predators_evolution(self, x, y):
        """
        x: proies
        y: predateurs
        """
        return y*(-self.g+self.d*x)

    def set_preys(self, alpha=0.8, beta=0.4):
        """
        a = taux de reproduction des proies
        b = taux de mortalité des proies dû aux prédateurs rencontrés
        """
        self.a, self.b = alpha, beta

    def set_predators(self, gamma=0.6, delta=0.2):
        """
        g = taux de mortalité des prédateurs
        d = taux de reproduction des prédateurs en fonction des proies rencontrées et mangées'''
        """
        self.g, self.d = gamma, delta

    def generate(self):
        del self.population[0:]
        h = (self.stop-self.start)/self.samples
        time, preys, predators = [
            0]*(self.samples+1), [0]*(self.samples+1), [0]*(self.samples+1)
        time[0] = self.start
        preys[0] = self.x
        predators[0] = self.y
        for i in range(self.samples):
            print("time", time[i])
            time[i+1] = time[0]+h*(i+1)
            print("preys", preys[i])
            preys[i+1] = preys[i]+h * \
                self.preys_evolution(preys[i], predators[i])
            predators[i+1] = predators[i]+h * \
                self.predators_evolution(preys[i], predators[i])
        self.population = zip(time, preys, predators)
        self.notify()
        return self.population


class Logistic(Subject):
    def __init__(self, r=np.linspace(0, 4, 1000), trials=50, niteration=100):
        Subject.__init__(self)
        self.r = r
        self.trials = trials
        self.niteration = niteration

    def iterations(self, r):
        x = random.uniform(0, 1)
        i = 0
        while i < self.niteration and x < 1:
            x = r*x*(1-x)
            i += 1
        return x if x < 1 else -1

    def generate(self):
        r_v = []
        x_v = []
        for rr in self.r:
            j = 0
            while j < self.trials:
                xx = self.iterations(rr)
                if xx > 0:               # Convergence: il s'agit d'une valeur d'équilibre
                    r_v.append(rr)
                    x_v.append(xx)
                j += 1                   # Nouvel essai

        return r_v, x_v


if __name__ == "__main__":
    a = 1
    while a != 0:
        a = input('choisir un chiffre entre 1 et 3 (sortie : 0) : ')
        if a in ('0', '1', '2', '3'):
            a = int(a)
            if a == 1:
                model = Generator()
                # # logger.debug("{}".format(model))
                print(model)
                signal = model.generate()
                time = [t[0] for t in signal]
                elongation = [e[1] for e in signal]
                plt.plot(time, elongation, ".g")
                model.set_steps(2)
                model.set_frequency(2.0)
                signal = model.generate()
                time = [t[0] for t in signal]
                elongation = [e[1] for e in signal]
                plt.plot(time, elongation, "or")
                model.set_samples(200)
                model.set_phase(90.0)
                signal = model.generate()
                time = [t[0] for t in signal]
                elongation = [e[1] for e in signal]
                plt.plot(time, elongation, "+b")
            elif a == 2:
                model = PreyPredator()
                signal = model.generate()
                signal = list(signal)
                time = [t[0] for t in signal]
                print(len(time))
                preys = [t[1] for t in signal]
                print(len(preys))
                predators = [t[2] for t in signal]
                print(len(predators))
                plt.plot(time, preys, "+g")
                plt.plot(time, predators, "-r")
                plt.plot(preys, predators, ".b")
            # r=np.linspace(0,4,100)
            # print(r)
            elif a == 3:
                model = Logistic()
                x, y = model.generate()
                plt.plot(x, y, 'r,')
                plt.xlabel('r')
                plt.ylabel('x')
            plt.show()
        else:
            print("Vous devez choisir un chiffre entre 1 et 3 !")

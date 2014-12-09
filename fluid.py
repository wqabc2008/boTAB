#/usr/bin/env python2
# -*- coding: utf-8 -*-

"""

boTAB
=====

This module contains classes and function for the modelling of droplets in
freestream flows

Author: Adam O'Brien

"""

from math import sqrt, pi

# Vector class for position/velocity

class Vector(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):

        return "%s, %s"%(self.x, self.y)

    def __add__(self, other):

        return Vector(self.x + other.x, self.y + self.y)

    def __sub__(self, other):

        return Vector(self.x - other.x, self.y - other.y)

    def mag(self):
        return sqrt(self.x**2 + self.y**2)

    def normalVector(self):
        return Vector(self.y, -self.x)

    def scale(self, other):
        return Vector(self.x*other, self.y*other)

    def rVector(self, other):

        return other - self

    def unitVector(self):

        return self.scale(1./self.mag())

def dot(u, v):

    return u.x*v.x + u.y*v.y

# Freestream class for representing the freestream flow

class Freestream(object):

    def __init__(self, rho, mu, temperature, k, velocity):
        self.rho = rho
        self.mu = mu
        self.temperature = temperature
        self.k = k
        self.velocity = velocity

# Droplet class for representing droplets

class Droplet(object):

    def __init__(self, radius, rho, mu, sigma, boilingTemp, latentHeat, specificHeat, k, position, velocity):
        self.radius = radius
        self.rho = rho
        self.mu = mu
        self.sigma = sigma
        self.boilingTemp = boilingTemp
        self.latentHeat = latentHeat
        self.specificHeat = specificHeat
        self.k = k
        self.position = position
        self.velocity = velocity
        self.mass = self.rho*(4./3.)*pi*self.radius**3
        self.area = pi*self.radius**2
        self.volume = self.mass/self.rho
        self.y = 0.
        self.dydt = 0.
        self.t = 0.

    def __repr__(self):

        return "Radius: %s\nPosition: %s\nVelocity: %s"%(str(self.radius), \
        self.position, self.velocity)

    def weberNo(self, freestream):

        vRel = self.velocity.rVector(freestream.velocity)

        return freestream.rho*dot(vRel, vRel)*self.radius/self.sigma

    def weberNoCrit(self, freestream, Cf, Ck, Cb):

        return Cf/(Ck*Cb)*self.weberNo(freestream)

    def td(self, Cd):

        return 2.*self.rho*self.radius ** 2/(Cd*self.mu)

    def omega(self, Cd, Ck):

        td = self.td(Cd)

        return sqrt(Ck*self.sigma/(self.rho*self.radius ** 3) - 1./td**2)

    def advect(self, freestream, Cb, dt):

        vRel = self.velocity.rVector(freestream.velocity)

        Fd = vRel.unitVector().scale(Cb*freestream.rho*dot(vRel, vRel)/2*self.area)

        a = Fd.scale(1./self.mass)

        self.position += self.velocity.scale(dt) + a.scale(dt**2/2)

        self.velocity += a.scale(dt)

    def checkBreakup(self):

        if self.y > 1.:
            return True
        else:
            return False
            
    def printAll(self):
        
        print "Radius:", self.radius
        print "Rho:", self.rho
        print "mu:", self.mu
        print "sigma:", self.sigma
        print "Boiling Temp:", self.boilingTemp
        print "Latent Heat:", self.latentHeat
        print "Specific Heat:", self.specificHeat
        print "k:", self.k
        print "Position:", self.position
        print "Velocity:", self.velocity

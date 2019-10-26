#!/usr/bin/env python
# coding: utf-8

# # Figure 7, page 7.1-149 of NAVFAC Soil Mechanics
# Figure 7 is typically used to estimate the angle of internal friction for soils assumed to be cohesionless, using either dry unit weight or relative density as inputs. Alternatively, the relative density can be estimated using the soil type and dry unit weight.
# 
# To use this figure, create an instance of fig_7. You can pass in gamma or relative density values as parameters.
# 
# fig = fig_7(gamma=120)
# 
# You can 

# In[1]:


class Fig_7():
    def __init__(self, gamma=None, relative_density=None, soil_type=None, void_ratio=None, porosity=None):
        #phi cannot be user defined
        self._phi = None

        #gamma
        try:
            if float(gamma) >= 75 and float(gamma) <= 150:
                self._gamma = float(gamma)
            else:
                print('gamma out of range. gamma must be between 75 and 150 pcf. No gamma value set.')
                self._gamma = None
        except:
            print('gamma must be a float between 75 and 150 pcf. No gamma value set.')
            self._gamma = None

        #relative_density
        try:
            if float(relative_density) >= 0 and float(relative_density) <= 100:
                self._relative_density = float(relative_density)
            else:
                print('relative_density out of range. relative_density must be between 0 and 100 percent. No relative_density value set.')
                self._relative_density = None
        except:
            print('relative_density must be a float between 0 and 100 percent. No relative_density value set.')
            self._relative_density = None

        #soil type
        if soil_type in ['ML','SM','SP','SW','GP','GW']:
            self._soil_type = soil_type
        else:
            print("soil_type must be in ['ML','SM','SP','SW','GP','GW']. No soil_type set.")

        #void_ratio
        try:
            if float(void_ratio) >= 0.15 and float(void_ratio) <= 1.2:
                self._void_ratio = float(void_ratio)
            else:
                print('void_ratio out of range. void_ratio must be between 0.15 and 1.2. No void_ratio value set.')
                self._void_ratio = None
        except:
            print('void_ratio must be a float between 0.15 and 1.2. No void_ratio value set.')
            self._void_ratio = None

        #porosity
        try:
            if float(porosity) >= 0.15 and float(porosity) <= 0.55:
                self._porosity = float(porosity)
            else:
                print('porosity out of range. porosity must be between 0.15 and 0.55. No porosity value set.')
                self._porosity = None
        except:
            print('porosity must be a float between 0.15 and 0.55. No porosity value set.')
            self._porosity = None
            
    #setters and getters       
    @property
    def gamma(self):
        try:
            return round(self._gamma,1)
        except:
            return self._gamma
    @gamma.setter
    def gamma(self, gamma):
        try:
            if float(gamma) >= 75 and float(gamma) <= 150:
                self._gamma = float(gamma)
            else:
                print('gamma out of range. gamma must be between 75 and 150 pcf. No gamma value set.')
        except:
            print('gamma must be a float between 75 and 150 pcf. No gamma value set.')

    @property
    def relative_density(self):
        try:
            return round(self._relative_density)
        except:
            return self._relative_density
    @relative_density.setter
    def relative_density(self, relative_density):
        try:
            if float(relative_density) >= 0 and float(relative_density) <= 100:
                self._relative_density = float(relative_density)
            else:
                print('relative_density out of range. relative_density must be between 0 and 100 percent. No relative_density value set.')
        except:
            print('relative_density must be a float between 0 and 100 percent. No relative_density value set.')

    @property
    def soil_type(self):
        return self._soil_type
    @soil_type.setter
    def soil_type(self, soil_type):
        if soil_type in ['ML','SM','SP','SW','GP','GW']:
            self._soil_type = soil_type
        else:
            print("soil_type must be in ['ML','SM','SP','SW','GP','GW']. No soil_type set.")

    @property
    def void_ratio(self):
        return self._void_ratio
    @void_ratio.setter
    def void_ratio(self, void_ratio):
        try:
            if float(void_ratio) >= 0.15 and float(void_ratio) <= 1.2:
                self._void_ratio = float(void_ratio)
            else:
                print('void_ratio out of range. void_ratio must be between 0.15 and 1.2. No void_ratio value set.')
        except:
            print('void_ratio must be a float between 0.15 and 1.2. No void_ratio value set.')

    @property
    def porosity(self):
        return self._porosity
    @porosity.setter
    def porosity(self, porosity):
        try:
            if float(porosity) >= 0.15 and float(porosity) <= 0.55:
                self._porosity = float(porosity)
            else:
                print('porosity out of range. porosity must be between 0.15 and 0.55. No porosity value set.')
        except:
            print('porosity must be a float between 0.15 and 0.55. No porosity value set.')
            
    @property
    def phi(self):
        try:
            return round(self._phi)
        except:
            return self._phi

    def get_gamma_from_relative_density(self):
        '''
        Reads dry unit weight from chart using relative density. 
        Sets gamma parameter and returns new value.
        '''
        soil_type_to_line_index = {'ML':0, 'SM':1, 'SP':2, 'GP':3, 'GW':4}
        density_ranges = [[79.5,98], [88,107], [102,124], [109.2,133.5], [117.5,145]]
        try:
            line_index = soil_type_to_line_index[self._soil_type]
            dry_density = ((self._relative_density / 100) * (density_ranges[line_index][1] 
                            - density_ranges[line_index][0]) + density_ranges[line_index][0])
        except:
            print("Set a soil_type and relative_density before calling get_gamma_from_relative_density().")
            return
        self._gamma = dry_density
        return dry_density
    
    def read_phi(self):
        '''
        Reads phi from chart. If gamma is not defined, it will first be determined from relative_density.
        '''
        soil_type_to_line_index = {'ML':0, 'SM':1, 'SP':2, 'GP':3, 'GW':4}
        slopes = [0.540541, 0.610526, 0.613636, 0.613169, 0.614545]
        intercepts = [-16.973, -27.5263, -35.5909, -39.6580, -44.3091]
        try:
            line_index = soil_type_to_line_index[self._soil_type]
        except:
            print('soil_type must be set before calling read_phi()')
            return
        try:
            self._phi = slopes[line_index] * self._gamma + intercepts[line_index]
            return self._phi
        except:
            try:
                self.get_gamma_from_relative_density()
                self._phi = slopes[line_index] * self._gamma + intercepts[line_index]
            except:
                print('gamma or relative_density must be set before calling read_phi()')
                return
            
    def get_relative_density_from_gamma(self):
        '''
        Reads relative density from chart using dry unit weight.
        Sets relative_density and returns new value.
        '''
        soil_type_to_line_index = {'ML':0, 'SM':1, 'SP':2, 'GP':3, 'GW':4}
        density_ranges = [[79.5,98], [88,107], [102,124], [109.2,133.5], [117.5,145]]
        try:
            line_index = soil_type_to_line_index[self._soil_type]
            self._relative_density = ((self._gamma - density_ranges[line_index][0]) / 
                                      (density_ranges[line_index][1] - density_ranges[line_index][0]) * 100)
            return self._relative_density
        except:
            print('soil_type and gamma must be set before calling get_relative_density_from_gamma()')
            return


# # Figure 3 - Estimate effective vertical stress from SPT blows and relative density

# In[2]:


class Fig_3():
    def __init__(self, relative_density=None, blows=None):
        self._eff_stress = None
        
        #relative_density
        try:
            if float(relative_density) >= 0 and float(relative_density) <= 100:
                self._relative_density = float(relative_density)
            else:
                print('relative_density out of range. relative_density must be between 0 and 100 percent. No relative_density value set.')
                self._relative_density = None
        except:
            print('relative_density must be a float between 0 and 100 percent. No relative_density value set.')
            self._relative_density = None
            
        #blows
        try:
            if int(blows) >= 0 and int(blows) <= 80:
                self._blows = int(blows)
            else:
                print('blows out of range. blows must be an integer between 0 and 80. No blows value set.')
                self._blows = None
        except:
            print('blows must be an integer between 0 and 80. No blows value set.')
            self._blows = None
        
    #setters and getters
    #relative density
    @property
    def relative_density(self):
        try:
            return round(self._relative_density)
        except:
            return self._relative_density
    @relative_density.setter
    def relative_density(self, relative_density):
        try:
            if float(relative_density) >= 0 and float(relative_density) <= 100:
                self._relative_density = float(relative_density)
            else:
                print('relative_density out of range. relative_density must be between 0 and 100 percent. No relative_density value set.')
        except:
            print('relative_density must be a float between 0 and 100 percent. No relative_density value set.')
            
    #blows
    @property
    def blows(self):
        return self._blows
    @blows.setter
    def blows(self, blows):
        try:
            if int(blows) >= 0 and int(blows) <= 80:
                self._blows = int(blows)
            else:
                print('blows out of range. blows must be an integer between 0 and 80. No blows value set.')
        except:
            print('blows must be an integer between 0 and 80. No blows value set.')
            
    #eff_stress
    @property
    def eff_stress(self):
        return self._eff_stress
    
    def read_eff_stress(self):
        '''
        Estimates the effective vertical stress in kips per square foot
        given relative density in percent and SPT blows per foot.
        Based on NAVFAC Figure 3 on page 7.1-87
        'Correlations Between Relative Density and Standard Penetration Resistance
        in Accordance with Gibbs and Holtz'
        Evaluates at two curves bracketing the input density and returns a weighted average.
        This method can give innacurate results when curves are evaluated at blow counts
        off the chart. The method tries to mitigate this by truncating the value to 6,
        but the results should still be used with caution.
        In all cases, this is an estimate anyway.
        
        TODO: Make this set self._eff_stress
        '''
        rd = self._relative_density
        #Define a curve for each relative density value as on the graph
        R15 = lambda x: 0.1*x**3 -0.45*x**2 + 0.95*x#
        R40 = lambda x: 0.00119048*x**3 + 0.0285714*x**2 + 0.120238*x - 0.36428#
        R50 = lambda x: -.0000601251*x**3 + 0.0232383*x**2 - 0.0102513*x - 0.24621#
        R60 = lambda x: 0.000169745*x**3 - 0.00129699*x**2 + 0.212685*x - 1.15878#
        R70 = lambda x: -.0000489081*x**3 + 0.005052*x**2 + 0.075252*x - 0.974614#
        R80 = lambda x: 0.000159039*x**2 + 0.141959*x - 1.65356#
        R85 = lambda x: 0.0000988373*x**2 + 0.124801*x - 1.63912#
        R90 = lambda x: 0.0000831169*x**2 + 0.107429*x - 1.63013#
        R100 = lambda x: -.00017024*x**2 + 0.10128*x - 1.86286#
        #Use a set of if/elif statements to determine which two curves bracket the query
        if rd >= 15 and rd <40:
            lower_curve = R15
            upper_curve = R40
            low_d = 15
            high_d = 40
        elif rd >= 40 and rd < 50:
            lower_curve = R40
            upper_curve = R50
            low_d = 40
            high_d = 50
        elif rd >= 50 and rd < 60:
            lower_curve = R50
            upper_curve = R60
            low_d = 50
            high_d = 60
        elif rd >= 60 and rd < 70:
            lower_curve = R60
            upper_curve = R70
            low_d = 60
            high_d = 70
        elif rd >= 70 and rd < 80:
            lower_curve = R70
            upper_curve = R80
            low_d = 70
            high_d = 80
        elif rd >= 80 and rd < 85:
            lower_curve = R80
            upper_curve = R85
            low_d = 80
            high_d = 85
        elif rd >= 85 and rd < 90:
            lower_curve = R85
            upper_curve = R90
            low_d = 85
            high_d = 90
        elif rd >= 90 and rd <= 100:
            lower_curve = R90
            upper_curve = R100
            low_d = 90
            high_d = 100
        else:
            print('relative density should be in the interval [15,100]')
            return
        #Evaluate the function using blows for each of the two curves bracketing the query
        lower_point = lower_curve(self._blows)
        upper_point = upper_curve(self._blows)
        #if lower point goes below curve, reduce value to 6 to help the estimate
        if lower_point > 6:
            print('Use caution. Evaluation of lower curve is off the chart.')
            lower_point = 6
        if upper_point > 6:
            upper_point = 6
            print('Use caution. Evaluation of upper curve is off the chart.')
        weighting_term = (rd - low_d) / (high_d - low_d)
        effective_stress = weighting_term * upper_point + (1 - weighting_term) * lower_point
        return round(effective_stress,1)


# # Drilled Shaft Design

# In[1]:





# In[30]:


class Drilled_Shaft_Design():
    unit_weight_water_pcf = 62.4
    unit_weight_concrete_pcf = 150
    phi_to_Nq_conversion_drilled_pier = {
                                          26: 5,
                                          27: 6.5, #not in NAVDAC
                                          28: 8,
                                          29: 9, #not in NAVDAC
                                          30: 10,
                                          31: 12,
                                          32: 14,
                                          33: 17,
                                          34: 21,
                                          35: 25,
                                          36: 30,
                                          37: 38,
                                          38: 43,
                                          39: 60,
                                          40: 72
                                        }
    phi_to_Nq_conversion_driven_pile = {
                                          26: 10,
                                          27: 12.5, #not in NAVDAC
                                          28: 15,
                                          29: 18, #not in NAVDAC
                                          30: 21,
                                          31: 24,
                                          32: 29,
                                          33: 35,
                                          34: 42,
                                          35: 50,
                                          36: 62,
                                          37: 77,
                                          38: 86,
                                          39: 120,
                                          40: 145
                                        }
    
    pile_type_to_K_compression = {'drilled pier' : 0.75,
                                  'driven single H-pile' : 1.25,
                                  'driven single displacement pile' : 1.75,
                                  'driven single displacement tapered pile' : 0.65,
                                  'driven jetted pile' : 0.7
                                  }
    pile_type_to_K_tension = {'drilled pier' : 0.4,
                              'driven single H-pile' : 0.75,
                              'driven single displacement pile' : 1.15,
                              'driven single displacement tapered pile' : 0.45,
                              'driven jetted pile' : 0.4
                              }

    
    def __init__(self, depth_water_table_feet=None, foundation_type=None, material=None, 
                 layer_thicknesses=None, layer_unit_weights=None, layer_phi_or_cs=None,
                sublayer_thickness=None, ignored_depth_feet=None):
        import math
        self._subdivided_thicknesses = None
        self._subdivided_unit_weights = None
        self._subdivided_phi_or_cs = None
        self._total_stress_profile = None
        self._pore_pressure_profile = None
        self._effective_stress_profile = None
        self._side_friction_profile = None
        
        #depth_water_table
        try:
            if float(depth_water_table_feet) >= 0:
                self._depth_water_table = depth_water_table_feet
            else:
                print('depth_water_table must be float value greater than or equal to 0. depth_water_table set to None.')
                self._depth_water_table = None
        except:
            print('depth_water_table must be float value greater than or equal to 0. depth_water_table set to None.')
            self._depth_water_table = None
            
        #foundation_type
        if foundation_type in ['drilled pier', 'driven single H-pile', 'driven single displacement pile',
                              'driven single displacement tapered pile', 'driven jetted pile']:
            self._foundation_type = foundation_type
        else:
            print("foundation_type must be in ['drilled pier', 'driven single H-pile', 'driven single displacement pile', 'driven single displacement tapered pile', 'driven jetted pile']. No foundation type set.")
            self._foundation_type = None
            
        #material
        if material in ['concrete', 'timber', 'steel']:
            self._material = material
        else:
            print("material must be in ['concrete', 'timber', 'steel']. No material set.")
            self._material = None
            
        #layer_thicknesses
        try:
            thicknesses = [float(thickness) for thickness in layer_thicknesses]
            valid = True
            for thickness in thicknesses:
                if thickness <= 0:
                    valid = False
            if not valid:
                print('Each layer in layer_thicknesses must be of type float and and greater than zero. No layer_thicknesses set.')
                self._layer_thicknesses = None
            else:
                self._layer_thicknesses = thicknesses
        except:
            print('Each layer in layer_thicknesses must be of type float and and greater than zero. No layer_thicknesses set.')
            self._layer_thicknesses = None
            
        #layer_unit_weights
        try:
            unit_weights = [float(unit_weight) for unit_weight in layer_unit_weights]
            valid = True
            for unit_weight in unit_weights:
                if unit_weight <= 0:
                    valid = False
            if not valid:
                print('Each layer in layer_unit_weights must be of type float and and greater than zero. No layer_unit_weights set.')
                self._layer_unit_weights = None
            else:
                self._layer_unit_weights = unit_weights
        except:
            print('Each layer in layer_unit_weights must be of type float and and greater than zero. No layer_unit_weights set.')
            self._layer_unit_weights = None    
            
        #layer_phi_or_c
        try:
            phi_or_cs = [float(phi_or_c) for phi_or_c in layer_phi_or_cs]
            valid = True
            for phi_or_c in phi_or_cs:
                if phi_or_c <= 0:
                    valid = False
            if not valid:
                print('Each layer in layer_phi_or_cs must be of type float and and greater than zero. No layer_phi_or_cs set.')
                self._layer_phi_or_cs = None
            else:
                self._layer_phi_or_cs = phi_or_cs
        except:
            print('Each layer in layer_phi_or_cs must be of type float and and greater than zero. No layer_phi_or_cs set.')
            self._layer_phi_or_cs = None          
            
        #sublayer_thickness
        try:
            if float(sublayer_thickness) > 0:
                self._sublayer_thickness = sublayer_thickness
            else:
                print('sublayer_thickness must be float value greater than 0. No sublayer_thickness set.')
                self._sublayer_thickness = None
        except:
            print('sublayer_thickness must be float value greater than 0. No sublayer_thickness set.')
            self._sublayer_thickness = None
            
        #ignored_depth_feet
        try:
            if float(ignored_depth_feet) >= 0:
                self._ignored_depth_feet = ignored_depth_feet
            else:
                print('ignored_depth_feet must be float value greater than or equal to 0. ignored_depth_feet set to None.')
                self._ignored_depth_feet = None
        except:
            print('ignored_depth_feet must be float value greater than or equal to 0. ignored_depth_feet set to None.')
            self._ignored_depth_feet = None
            
    @property
    def depth_water_table(self):
        return self._depth_water_table
    @depth_water_table.setter
    def depth_water_table(self,depth_water_table_feet):
        try:
            if float(depth_water_table_feet) >= 0:
                self._depth_water_table = depth_water_table_feet
            else:
                print('depth_water_table must be float value greater than or equal to 0. depth_water_table not set.')
        except:
            print('depth_water_table must be float value greater than or equal to 0. depth_water_table not set.')
            
    @property
    def foundation_type(self):
        return self._foundation_type
    @foundation_type.setter
    def foundation_type(self, foundation_type):
        if foundation_type in ['drilled pier', 'driven single H-pile', 'driven single displacement pile',
                              'driven single displacement tapered pile', 'driven jetted pile']:
            self._foundation_type = foundation_type
        else:
            print("foundation_type must be in ['drilled pier', 'driven single H-pile', 'driven single displacement pile', 'driven single displacement tapered pile', 'driven jetted pile']. No foundation type set.")
      
    @property
    def material(self):
        return self._material
    @material.setter
    def material(self, material):
        if material in ['concrete', 'timber', 'steel']:
            self._material = material
        else:
            print("material must be in ['concrete', 'timber', 'steel']. No material set.")
            
    @property
    def layer_thicknesses(self):
        return self._layer_thicknesses
    @layer_thicknesses.setter
    def layer_thicknesses(self, layer_thicknesses):
        try:
            thicknesses = [float(thickness) for thickness in layer_thicknesses]
            valid = True
            for thickness in thicknesses:
                if thickness <= 0:
                    valid = False
            if not valid:
                print('Each layer in layer_thicknesses must be of type float and and greater than zero. No layer_thicknesses set.')
            else:
                self._layer_thicknesses = thicknesses
        except:
            print('Each layer in layer_thicknesses must be of type float and and greater than zero. No layer_thicknesses set.')
        
    @property
    def layer_unit_weights(self):
        return self._layer_unit_weights
    @layer_unit_weights.setter
    def layer_unit_weights(self, layer_unit_weights):
        try:
            unit_weights = [float(unit_weight) for unit_weight in layer_unit_weights]
            valid = True
            for unit_weight in unit_weights:
                if unit_weight <= 0:
                    valid = False
            if not valid:
                print('Each layer in layer_unit_weights must be of type float and and greater than zero. No layer_unit_weights set.')
            else:
                self._layer_unit_weights = unit_weights
        except:
            print('Each layer in layer_unit_weights must be of type float and and greater than zero. No layer_unit_weights set.')  
            
    @property
    def layer_phi_or_cs(self):
        return self._layer_phi_or_cs
    @layer_phi_or_cs.setter
    def layer_phi_or_cs(self, layer_phi_or_cs):
        try:
            phi_or_cs = [float(phi_or_c) for phi_or_c in layer_phi_or_cs]
            valid = True
            for phi_or_c in phi_or_cs:
                if phi_or_c <= 0:
                    valid = False
            if not valid:
                print('Each layer in layer_phi_or_cs must be of type float and and greater than zero. No layer_phi_or_cs set.')
            else:
                self._layer_phi_or_cs = phi_or_cs
        except:
            print('Each layer in layer_phi_or_cs must be of type float and and greater than zero. No layer_phi_or_cs set.')
        
    @property
    def sublayer_thickness(self):
        return sublayer_thickness
    @sublayer_thickness.setter
    def sublayer_thickness(self, sublayer_thickness):
        try:
            if float(sublayer_thickness) > 0:
                self._sublayer_thickness = sublayer_thickness
            else:
                print('sublayer_thickness must be float value greater than 0. No sublayer_thickness set.')
        except:
            print('sublayer_thickness must be float value greater than 0. No sublayer_thickness set.')
            
    @property
    def total_stress_profile(self):
        return self._total_stress_profile
    
    @property
    def pore_pressure_profile(self):
        return self._pore_pressure_profile
    
    @property
    def effective_stress_profile(self):
        return self._effective_stress_profile
    
    @property
    def side_friction_profile(self):
        return self._side_friction_frofile
    
    @property
    def ignored_depth_feet(self):
        try:
            if float(ignored_depth_feet) >= 0:
                self._ignored_depth_feet = ignored_depth_feet
            else:
                print('ignored_depth_feet must be float value greater than or equal to 0. ignored_depth_feet set to None.')
        except:
            print('ignored_depth_feet must be float value greater than or equal to 0. ignored_depth_feet set to None.')
        
        
    def convert_pounds_to_kips(self, pounds):
        '''
        1 kip = 1000 pounds
        '''
        return pounds/1000
    
    def calculate_area_from_diameter(self, diameter_feet):
        '''
        A = pi*r^2
        '''
        return math.pi * (diameter_feet / 2)**2
    
    def calculate_weight_of_foundation_pounds(self, diameter_feet, embedment_depth_feet):
        '''
        w = Vol * unit weight, above water table
        w = Vol * buoyant unit weight, below water table
        '''
        if embedment_depth_feet < self._depth_water_table:
            return self.calculate_area_from_diameter(diameter_feet) * embedment_depth_feet * self.unit_weight_concrete_pcf
        else:
            return (self.calculate_area_from_diameter(diameter_feet) * 
                    (self._depth_water_table * self.unit_weight_concrete_pcf + 
                     (embedment_depth_feet - self._depth_water_table) * (self.unit_weight_concrete_pcf - self.unit_weight_water_pcf)))
        
    def phi_to_Nq(self, phi):
        '''
        Get Nq from lookup table. Value if different for drilled piers vs driven piles.
        '''
        if self._foundation_type == 'drilled pier':
            return self.phi_to_Nq_conversion_drilled_pier[phi]
        elif self._foundation_type != None: #for driven piles
            return self.phi_to_Nq_conversion_driven_pile[phi] 
        
    def end_bearing_granular(self, effective_stress_ksf, phi, diameter_feet):
        '''
        Calculate the end bearing in ksf 
        DOUBLE CHECK UNITS ON EFFECTIVE STRESS
        '''
        Nq = self.phi_to_Nq(phi)
        At = self.calculate_area_from_diameter(diameter_feet)
        return effective_stress_ksf * Nq * At
    
    def cohesion_to_adhesion(self, c):
        '''
        Converts cohesion to adhesion.
        NEED TO FIGURE OUT WHAT THE UNITS ARE AND CLARIFY FOR DOCUMENTATION
        '''
      #This assumes concrete or timber pile
      # a = bottom of a range + (c - min in c range) / c range * range of a
        if c < 250:
            a = c
        elif c < 500: #adhesion range 250-480
            a = 250. + (c - 250.) / 250 *  230
        elif c < 1000: #480-750
            a = 480. + (c - 500) / 500 * 270
        elif c < 2000: #750-950
            a = 750 + (c - 1000) / 1000 * 200
        elif c < 4000: #950-1300
            a = 950 + (c - 2000) / 2000 * 350
        else:
            a = 1300
        return a
    
    def bearing_capacity_factor_cohesive(self, embedment_depth_feet, diameter_feet):
        '''
        Reads the bearing capacity factor for cohesive soils given embedment depth and diameter.
        DOUBLE CHECK ON SOURCE. I THINK I FIT A CURVE FROM A CHART HERE
        '''
        x = embedment_depth_feet / diameter_feet
        if x < 4:
            return 6.29 + 1.88*x + -.506*x**2 + .0632*x**3 + -.0031*x**4;
        else:
            return 9
        
    def end_bearing_kips_cohesive(self, cohesion, embedment_depth_feet, diameter_feet):
        '''
        Calculate the end bearing for a cohesive layer
        '''
        return (cohesion * self.calculate_area_from_diameter(diameter_feet) 
                * self.bearing_capacity_factor_cohesive(embedment_depth_feet, diameter_feet))
    def side_friction_kips_cohesive(self, layer_thickness_feet, cohesion, diameter_feet):
        '''
        Calculates the side friction for a cohesive layer.
        CHECK ON UNITS HERE
        '''
        return math.pi * diameter_feet * layer_thickness_feet * self.cohesion_to_adhesion(cohesion)
    
    def internal_friction_to_contact_friction(self, phi): 
        '''
        Calculates contact friction angle as a function of material and internal friction angle
        '''
        if self._material == 'concrete':
            return 0.75 * phi
        else:
            return 20
        
    def earth_pressure_coefficient(self, is_compressive):
        '''
        Calculate earth pressure coefficient based on pile type and whether pile is in tension or compression
        '''
        if is_compressive:
            return self.pile_type_to_K_compression[self._foundation_type]
        else:
            return self.pile_type_to_K_tension[self._foundation_type]
        
    def side_friction_granular(self, layer_thickness_feet, phi, effective_stress_ksf, is_compressive, diameter_feet):
        '''
        CHECK UNITS
        '''
        return (self.earth_pressure_coefficient(is_compressive) * effective_stress_ksf 
                * math.tan(self.internal_friction_to_contact_friction(phi) * math.pi / 180) 
                * math.pi * diameter_feet * layer_thickness_feet)
    
    def create_subdivided_soil_profile(self):
        '''
        Creates a subdivided soil profile for more accurate calculations.
        There is a lot of wasted calculation here since as it turns out, the layer size
        only matters for granular layers. Subdividing the layers does nothing for cohesive soils.
        However, this analysis does not take long to run, so there is no reason to spend time
        optimizing to only subdivide the granular layers.
        '''
        if (len(self._layer_thicknesses) != len(self._layer_unit_weights) 
            and len(self._layer_thicknesses) != len(self._layer_phi_or_cs)):
            raise IndexError('layer_thicknesses, layer_unit_weights, and layer_phi_or_cs must all be of the same length')
        self._subdivided_thicknesses = []
        self._subdivided_unit_weights = []
        self._subdivided_phi_or_cs = []
        for i in range(len(self._layer_thicknesses)):
            layer_thickness = self._layer_thicknesses[i]
            num_sublayers = int(layer_thickness / self._sublayer_thickness)
            for j in range(num_sublayers):
                self._subdivided_thicknesses.append(self._sublayer_thickness)
                self._subdivided_unit_weights.append(self._layer_unit_weights[i])
                self._subdivided_phi_or_cs.append(self._layer_phi_or_cs[i])
        return self._subdivided_thicknesses, self._subdivided_unit_weights, self._subdivided_phi_or_cs
    
    def create_total_stress_profile(self):
        '''
        Generates total stress profile from existing subdivided soil profile. 
        Will throw error if called before create_subdivided_soil_profile().
        Total stress = unit weight * depth
        '''
        self._total_stress_profile = []
        total_stress = 0
        for i in range(len(self._subdivided_thicknesses)):
            total_stress += self._subdivided_thicknesses[i] * self._subdivided_unit_weights[i]
            self._total_stress_profile.append(total_stress)
        return self._total_stress_profile
    
    def create_pore_pressure_profile(self):
        '''
        Generates pore pressure profile from existing subdivided soil profile and water table depth. 
        Will throw error if called before create_subdivided_soil_profile() and initializing water_table_depth_Feet.
        Pore pressure = 0 above water table, unit weight of water * depth below water table
        '''
        self._pore_pressure_profile = []
        pore_pressure = 0
        depth = 0
        for i in range(len(self._subdivided_thicknesses)):
            depth += self._subdivided_thicknesses[i]
            if depth > self._depth_water_table:
                pore_pressure += self.unit_weight_water_pcf * self._subdivided_thicknesses[i]
            self._pore_pressure_profile.append(pore_pressure)
        return self._pore_pressure_profile
    
    def create_effective_stress_profile(self, diameter_feet):
        '''
        Generates effective stress profile from existing total stress profile and pore pressure profile.
        Effective stress = total stress - pore pressure
        According to this NAVFAC design, effective stress stops increasing at a depth
        of 20 diameters.
        '''
        self._effective_stress_profile = []
        depth = 0
        for i in range(len(self._subdivided_thicknesses)):
            depth += self._subdivided_thicknesses[i]
            if depth <= 20 * diameter_feet:
                effective_stress = self._total_stress_profile[i] - self._pore_pressure_profile[i]
            else: #effective stress stops increasing at 20*D
                effective_stress = self._effective_stress_profile[i-1]
            self._effective_stress_profile.append(effective_stress)
        return self._effective_stress_profile
    
    def create_side_friction_profile(self, is_compressive, diameter_feet):
        '''
        Generates side friction profile from existing properties.
        Soil properties must be fully defined before calling this function.
        '''
        self._side_friction_profile = []
        #set side friction to ignored_depth_feet equal to zero
        for i in range(int(self._ignored_depth_feet / self._sublayer_thickness)):
            self._side_friction_profile.append(0)
            #start counting side friction for either granular or cohesive layer
        for i in range(int(self._ignored_depth_feet / self._sublayer_thickness), len(self._subdivided_phi_or_cs)):
            if self._subdivided_phi_or_cs[i] < 100: #granular layer
                side_friction = self.side_friction_granular(self._sublayer_thickness, self._subdivided_phi_or_cs[i]
                                                            , self._effective_stress_profile[i], is_compressive, diameter_feet)
            else:
                side_friction = self.side_friction_kips_cohesive(self._sublayer_thickness, self._subdivided_phi_or_cs[i], diameter_feet)
            self._side_friction_profile.append(side_friction)
        return self._side_friction_profile
    
    def calculate_ultimate_side_friction(self, embedment_depth):
        '''
        Calculates total side friction over the length of the pile in pounds
        '''
        self._ultimate_side_friction = 0
        depth = 0
        for i in range(len(self._side_friction_profile)):
            depth += self._sublayer_thickness
            if depth <= embedment_depth:
                self._ultimate_side_friction += self._side_friction_profile[i]
            else:
                break
        return self._ultimate_side_friction    
    
    def calculate_ultimate_toe_bearing(self, embedment_depth, diameter_feet, is_compressive):
        '''
        Calculates toe bearing in pounds
        '''
        if is_compressive == False:
            return 0 #no toe bearing in tension
        elif self._subdivided_phi_or_cs[int(embedment_depth / self._sublayer_thickness)] < 100: #if layer BENEATH embedment is granular
            return self.end_bearing_granular(self._effective_stress_profile[int(embedment_depth / self._sublayer_thickness) - 1], self._subdivided_phi_or_cs[int(embedment_depth / self._sublayer_thickness)], diameter_feet) #calc end bearing based on stress AT embedment
        else:
            return self.end_bearing_kips_cohesive(self._subdivided_phi_or_cs[int(embedment_depth / self._sublayer_thickness)], embedment_depth, diameter_feet)

    def calculate_allowable_load(self, ultimate_side_friction, ultimate_toe_bearing, is_compressive, diameter_feet, embedment_depth, factor_of_safety):
        if is_compressive:
            return (ultimate_side_friction + ultimate_toe_bearing) / factor_of_safety
        else:
            return (ultimate_side_friction + ultimate_toe_bearing) / factor_of_safety + self.calculate_weight_of_foundation_pounds(diameter_feet, embedment_depth)       
        
    def analyze_pile(self, diameter_feet, embedment_depth, is_compressive, factor_of_safety):
        total_stress_profile = self.create_total_stress_profile()
        pore_pressure_profile = self.create_pore_pressure_profile()
        effective_stress_profile = self.create_effective_stress_profile(diameter_feet)
        side_friction_profile = self.create_side_friction_profile(is_compressive, diameter_feet)
        ultimate_side_friction = self.calculate_ultimate_side_friction(embedment_depth)
        ultimate_toe_bearing = self.calculate_ultimate_toe_bearing(embedment_depth, diameter_feet, is_compressive)
        allowable_load = self.convert_pounds_to_kips(self.calculate_allowable_load(ultimate_side_friction, ultimate_toe_bearing, is_compressive, diameter_feet, embedment_depth, factor_of_safety))
        print("Diameter = %d   Depth = %d     Allowable load = %d " % (diameter_feet, embedment_depth, allowable_load))        
        
    def analyze_range(self,diameter_list, embedment_list, is_compressive, factor_of_safety):
        if is_compressive:
            print("----\nEvaluating deep foundation in compression\n")
        else:
            print("----\nEvaluating deep foundation in tension\n")
        for diameter in diameter_list:
            for embedment in embedment_list:
                self.analyze_pile(diameter, embedment, is_compressive, factor_of_safety)
                print('')
            print('')








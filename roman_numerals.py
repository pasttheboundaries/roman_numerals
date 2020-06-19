# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 18:26:43 2020
roman numerals
@author: mdkgo
"""


class RomanDigit() :
    ''' A '''
    
    dictionary = {'i' : 1,
                  'v' : 5,
                  'x' : 10,
                  'l' : 50,
                  'c' : 100,
                  'd' : 500,
                  'm' : 1000}
    
    
    def __init__ (self, digit):
        self.digit = digit.lower()
        if self.digit not in self.dictionary:
            #print('Error: not roman digit')
            raise IllegalDigitError
    def decimal (self):
        return self.dictionary[self.digit]
    
    def __repr__ (self):
        return self.digit
    
    def __lt__ (self, other):
        # print (other)
        # print(type(other))
        # if other is not RomanDigit:
        #     raise IllegalDigitError
        return self.dictionary[self.digit] < self.dictionary[other.digit]
    
    def __gt__ (self, other):
        return self.dictionary[self.digit] > self.dictionary[other.digit]
        
    def __eq__ (self, other):
        return self.dictionary[self.digit] == self.dictionary[other.digit]
    # def __str__(self):
    #     print (self.digit)

    
class IllegalDigitError (Exception):
    pass

class IllegalNumeralError (Exception):
    pass
    

class RomanNumeral:
    ''' has only 2 attributes : RomanNumeral.roman and ROmanNumeral.decimal '''
    ddictionary = {1 : 'i',
                   5 : 'v',
                   10 : 'x',
                   50 : 'l',
                   100 : 'c',
                   500 : 'd',
                   1000 : 'm'}
    
    def __init__ (self, numeral):
        if type(numeral) == int:
            self.decimal = numeral
            self.roman = self.to_roman()
        elif type(numeral) == str:
            try:
                self.roman = numeral.lower()
                self.Rnumeral_list = []
                for digit in self.roman:
                    self.Rnumeral_list.append(RomanDigit(digit))
                self.decimal = self.to_decimal()
            except:
                for sign in numeral:
                    if sign.isdigit() == False:
                        raise IllegalNumeralError ('neither legal roman nor decimal numeral')
                self.decimal = int(numeral)
                self.roman = self.to_roman()
                
        else:
            raise IllegalNumeralError ('only str or int allowed')
            
    
    def to_roman (self):
        if self.decimal > 3999 or self.decimal < 1:
            raise IllegalNumeralError ('only 1 - 3999 allowed')
        roman = ''
        decimal = self.decimal
        if decimal // 1000 != 0:
            #koduj tysiące
            roman += 'm'*(decimal//1000)
        decimal = decimal - (decimal // 1000)*1000
        if decimal // 100 != 0:
            dhundrets = decimal // 100
            if (decimal-decimal % 100) in self.ddictionary:
                roman += self.ddictionary[(decimal-decimal % 100)]
            elif dhundrets <4:
                roman += 'c'*(decimal//100)
            elif dhundrets  == 4:
                roman += 'cd'
            elif dhundrets < 9:
                roman += 'd'+('c'*((decimal//100)-5))
            else:
                roman += 'cm'
        decimal = decimal - (decimal // 100)*100
        if decimal // 10 != 0:
            dtens = decimal // 10
            if (decimal-decimal % 10) in self.ddictionary:
                roman += self.ddictionary[(decimal-decimal % 10)]
            elif dtens <4:
                roman += 'x'*(decimal//10)
            elif dtens  == 4:
                roman += 'xl'
            elif dtens < 9:
                roman += 'l'+('x'*((decimal//10)-5))
            else:
                roman += 'xc'
        decimal = decimal - (decimal // 10)*10
        if decimal != 0:
            if decimal in self.ddictionary:
                roman += self.ddictionary[decimal]
            elif decimal <4:
                roman += 'i'*decimal
            elif decimal  == 4:
                roman += 'iv'
            elif decimal < 9:
                roman += 'v'+('i'*(decimal-5))
            else:
                roman += 'ix'
        return roman
                        
    
    def to_decimal (self):
        length = len(self.Rnumeral_list)
        aggregates = []
        decimal = 0
        skip = 0
        for index in range (0 , len(self.Rnumeral_list)):
            digit = self.Rnumeral_list[index]
            
            # if  index + 1 == length:
            #     decimal += digit.decimal()
            #     return decimal
            if skip > 0:
                skip -= 1
                continue
            aggregate, skip = self.find_aggregates (digit, self.Rnumeral_list[index :  ] )
            aggregates.append(aggregate)
        self.check_illegal(aggregates)
        decimal = self.sum_aggregates (aggregates)
        return decimal
    
    def find_aggregates (self, digit, Rn_list):
        skip = -1
        aggregate = []
        for ndigit in Rn_list:
            if ndigit == digit:
                aggregate.append(ndigit)
                skip += 1
                #print ('skip', skip)
                continue
            else:
                break
        return aggregate , skip  
            
    def check_illegal(self, aggregates):
        fives = 'vld'
        for aggregate in aggregates:
            if len(aggregate) > 1:
                if str(aggregate[0]) in fives:
                    raise IllegalNumeralError (str(aggregate[0]).upper() + ' can not be used more than once in a row')
            if len(aggregate) > 3:
                raise IllegalNumeralError ('no 4 digits in a row allowed')
            doublenumber = 0
            for double in aggregates:
                if double[0] == aggregate[0]:
                    doublenumber += 1
                    if doublenumber > 2:
                        raise IllegalNumeralError (str(double[0]).upper() +' in more than 2 positions')
        for ind in range(0, len(aggregates)):
            if ind == len(aggregates)-1:
                break
            if str(aggregates[ind+1][0]) in fives:
                if (aggregates[ind][0] < aggregates[ind+1][0] 
                    and aggregates[ind][0].decimal() != aggregates[ind+1][0].decimal()/5):
                    raise IllegalNumeralError ('incorrect digit subtracting from multiple of 5')
            else:
                if (aggregates[ind][0] < aggregates[ind+1][0] 
                    and aggregates[ind][0].decimal() != aggregates[ind+1][0].decimal()/10):
                    raise IllegalNumeralError ('numeral not allowed')
            if (aggregates[ind][0] < aggregates[ind+1][0] 
                and len(aggregates[ind]) > 1):
                raise IllegalNumeralError ('doubled digit on the left while subtracting')
            if aggregates[ind][0]<aggregates[ind+1][0] and len(aggregates[ind+1])>1:
                raise IllegalNumeralError ('doubled digit on the right while subtracting')
            if ind>0:
                if aggregates[ind-1][0] == aggregates[ind+1][0] and aggregates[ind-1][0] < aggregates[ind][0]:
                    raise IllegalNumeralError ('construction aba not allowed')
                if aggregates[ind-1][0].decimal() == aggregates[ind+1][0].decimal()*5 and aggregates[ind-1][0] < aggregates[ind][0]:
                    raise IllegalNumeralError ("can not subtract and add on both sides of the digit")
                if aggregates[ind-1][0].decimal()*5 == aggregates[ind+1][0].decimal() and aggregates[ind-1][0] < aggregates[ind][0]:
                    raise IllegalNumeralError ('can not subtract and add on both sides of the digit')
                if str(aggregates[ind-1][0]) == str(aggregates[ind+1][0]) and str(aggregates[ind-1][0]) in fives:
                    raise IllegalNumeralError ('can not subtract and add on both sides of the digit')
                    
                    
    
    def sum_aggregates (self, aggregates):
        decimal = 0
        skip = 0
        for index in range(0,len(aggregates)):
            if skip == 1:
                skip = 0
                continue
            if index+1 ==  len(aggregates):
                decimal += len(aggregates[index])*aggregates[index][0].decimal()
            else:
                if aggregates[index+1][0] > aggregates[index][0]:
                    decimal += (len(aggregates[index+1])*aggregates[index+1][0].decimal()
                                -len(aggregates[index])*aggregates[index][0].decimal())
                    skip = 1
                else:
                    decimal += len(aggregates[index])*aggregates[index][0].decimal()
                
        return decimal
        
    def __str__(self):
        return self.roman.upper()
    
    def __repr__ (self):
        return self.roman.upper()
    
    




    



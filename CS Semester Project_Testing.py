#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 20:46:33 2021

@author: manpreetdhindsa
"""

import unittest
from CS_Final_Project_Code import * 

# Used unittest library to conduct unit testing 
# Used appropriate format to conduct unit testing (writing test in file name, unittest.TestCase, etc.)
# Used asssertEquals to determine if th correct max value for the obsereved categories for points, rebounds, assists, blocks, and PER in the Top-5 starting analysis was collected
# Used assertEquals to determine that the correct players associated with the max value were found
# Used assertEquals to determine that the correct MVPs in each obsereved season were collected for the LeBron James vs MVP analysis 

class TestProject(unittest.TestCase):

	def test_top_Points(self): # Test to find max value of points in data set using assertEqual

		self.assertEqual(maxPoints, 36.1)

	def test_top_Rebs(self): # Test to find max value of rebounds in data using assertEqual

		self.assertEqual(maxReb, 15.6)	

	def test_top_Assists(self): # Test to find max value of assists in data set using assertEqual

		self.assertEqual(maxAssist, 11.6)

	def test_top_Blocks(self): # Test to find max value of blocks in data set using assertEqual

		self.assertEqual(maxBlocks, 2.9)

	def test_top_PER(self): # Test to find max value of PER using assertEqual

		self.assertEqual(maxPER, 31.94)

	def test_PPG_Leader(self): # Test to find player with max points using assertEqual

		self.assertEqual(myTopFive[0], "James Harden")

	def test_RPG_Leader(self): # Test to find player with max rebounds using assertEqual

		self.assertEqual(myTopFive[1], "Andre Drummond")

	def test_APG_Leader(self): # Test to find player with max assists using assertEqual

		self.assertEqual(myTopFive[2], "Steve Nash")

	def test_BPG_Leader(self): # Test to find player with max blocks using assertEqual

		self.assertEqual(myTopFive[3], "Tim Duncan")

	def test_PER_Leader(self): # Test to find player with max PER using assertEqual

		self.assertEqual(myTopFive[4], "Giannis Antetokounmpo")

	def test_MVP0(self): # Test to find the first MVP of our observed seasons using assertEquals

		self.assertEqual(theMVPList[0], "Kevin Garnett")

	def test_MVP1(self): # Test to find the second MVP of our observed seasons using assertEquals

		self.assertEqual(theMVPList[1], "Steve Nash")

	def test_MVP2(self): # Test to find the third MVP of our observed seasons using assertEquals

		self.assertEqual(theMVPList[2], "Steve Nash")

	def test_MVP3(self): # Test to find the fourth MVP of our observed seasons using assertEquals

		self.assertEqual(theMVPList[3], "Dirk Nowitzki")

	def test_MVP4(self): # Test to find the fifth MVP of our observed seasons using assertEquals

		self.assertEqual(theMVPList[4], "Kobe Bryant")

	def test_MVP5(self): # Test to find the sixth MVP of our observed seasons using assertEquals

		self.assertEqual(theMVPList[5], "Derrick Rose")

	def test_MVP6(self): # Test to find the seventh MVP of our observed seasons using assertEquals

		self.assertEqual(theMVPList[6], "Kevin Durant")

	def test_MVP7(self): # Test to find the eighth MVP of our observed seasons using assertEquals

		self.assertEqual(theMVPList[7], "Stephen Curry")

	def test_MVP8(self): # Test to find the ninth MVP of our observed seasons using assertEquals

		self.assertEqual(theMVPList[8], "Stephen Curry")

	def test_MVP9(self): # Test to find the tenth MVP of our observed seasons using assertEquals

		self.assertEqual(theMVPList[9], "Russell Westbrook")

	def test_MVP10(self): # Test to find the eleventh MVP of our observed seasons using assertEquals

		self.assertEqual(theMVPList[10], "James Harden")

	def test_MVP11(self): # Test to find the twelth MVP of our observed seasons using assertEquals

		self.assertEqual(theMVPList[11], "Giannis Antetokounmpo")

	def test_MVP12(self): # Test to find the thirteenth MVP of our observed seasons using assertEquals

		self.assertEqual(theMVPList[12], "Giannis Antetokounmpo")

class PointsSortCheckTestCase (unittest.TestCase):
  # Test if list is sorting properly
  def test_sort_pointspergame(self):
    # Read in the data
    dfcheck = df.copy()
    # Groupby the mean values of each player
    dfcheck = round(dfcheck.groupby(['Player Name']).mean(), 2)

    # Sort the values in order of Points per game
    dfsorted = dfcheck.sort_values(['Points Per Game'], ascending = False)
    
    # Get the first two players on the list
    listall = list(dfsorted.index)
    result1 = listall[0]
    result2 = listall[1]
    # These are the expected values
    expected1 = 'Allen Iverson'
    expected2 = 'James Harden'
    
    # Assert the expected values are equal to the result values
    self.assertEqual(expected1, result1)
    self.assertEqual(expected2, result2)

class FGRankTestCase (unittest.TestCase):
  # Test if rank is working properly
  def test_rank_FGPercent(self):
    # REad in the data
    dffg = df.copy()
    # Groupby the mean values of each player
    dffg = round(dffg.groupby(['Player Name']).mean(), 2)
    # Rank the data in order of Field Goal Percentage
    dffg['FGPercentRank'] = dffg['Field Goal Percentage'].rank(method='min',ascending = False)
    # Sort the values in order of Field Goal Percentage ranked value
    dffgsort = dffg.sort_values(['FGPercentRank'], ascending = True)
    
    # Get the first two players on the list
    listfg = list(dffgsort.index)
    resultone = listfg[0]
    resulttwo = listfg[1]
    # These are the expected values
    expectedone = 'Clint Capela'
    expectedtwo = 'Shaquille O\'Neal'
    
    # Assert the expected values are equal to the result values
    self.assertEqual(expectedone, resultone)
    self.assertEqual(expectedtwo, resulttwo)
    
    
number_of_rows = len(allseasons) #check the number of rows in the allseasons series
numberC = len(C3n) #check the number of rows in the Centers series
numberG = len(G3n) #check the number of rows in the Guards series
numberPG = len(PG3n) #check the number of rows in the Poitn Guards series
numberSG = len(SG3n) #check the number of rows in the Shooting Guards series
numberF = len(F3n) #check the number of rows in the Forwards series
numberSF = len(SF3n) #check the number of rows in the SFs series
numberPF = len(PF3n) #check the number of rows in the Power Forwards series

all = numberC + numberF + numberG + numberPF +numberPG +numberSF+numberSG #find the sum of all of those values

assert number_of_rows == all #assert that the total # of rows equal the sum of all the grouped rows

number_of_rows_final = len(Final) #check the number of rows in the allseasons series
countC = len(C) #check the number of rows in the Cs series
countG = len(G) #check the number of rows in the Gs series
countPG = len(PG) #check the number of rows in the PGs series
countSG = len(SG) #check the number of rows in the SGs series
countF = len(F) #check the number of rows in the Fs series
countSF = len(SF) #check the number of rows in the SFs series
countPF = len(PF) #check the number of rows in the PFs series

assert number_of_rows_final == 19 #assert that the number of rows equals the correct amount

assert countC == 19 #assert that each series has the correct number of rows
assert countG == 19 #assert that each series has the correct number of rows
assert countPG == 19 #assert that each series has the correct number of rows
assert countSG == 19 #assert that each series has the correct number of rows
assert countF == 19 #assert that each series has the correct number of rows
assert countSF == 19 #assert that each series has the correct number of rows
assert countPF == 19#assert that each series has the correct number of rows

if __name__ == '__main__':
    unittest.main()  















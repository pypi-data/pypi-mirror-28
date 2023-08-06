#encoding:utf-8
from functions import insertVoteWeb, checkDate, checkQuestionOp, checkOnlyOneVotePerUser, checkQuestionOpInPoll
import unittest
import datetime
from exceptions import PollDateException, NoQuestionOptionException, MoreThanOneVoteException
from models import Poll, UserAccount, Vote

class TestInsertMethods(unittest.TestCase):

    def testInsertVote(self):
        Vote.objects.all().delete()
        testPoll = Poll.objects.get(id = 1) 
        testPoll.startdate = datetime.datetime.strptime("2010-2-12", '%Y-%m-%d').date()
        testPoll.save() 
        testUser = UserAccount.objects.get(id = 1)
        testQuestionOptions = "12&56"
        testInsert = insertVoteWeb(testPoll.id, testUser.id, testQuestionOptions)
        self.assertIsNotNone(testInsert, "Error en la insercion del voto")
        Vote.objects.all().delete()
        
    def testCheckDate(self):
        testPoll = Poll.objects.get(id = 2) 
        self.assertRaises(PollDateException, checkDate, testPoll.id)
        
    def testCheckQuestionOp(self):
        self.assertRaises(NoQuestionOptionException, checkQuestionOp,"114&512&71")
        
    def testCheckQuestionOpInPoll(self):
        self.assertRaises(NoQuestionOptionException, checkQuestionOpInPoll, 1, "12&53")
        
    def testIncreasePollVotes(self):
        Vote.objects.all().delete()
        testPoll = Poll.objects.get(id = 1) 
        testPoll.votos_actuales = 0
        testPoll.save()
        testPoll.startdate = datetime.datetime.strptime("2010-2-12", '%Y-%m-%d').date()
        testPoll.save() 
        
        testUser1 = UserAccount.objects.get(id = 1)
        testUser2 = UserAccount.objects.get(id = 2)
        
        testQuestionOptions = "12&56"
        insertVoteWeb(testPoll.id, testUser1.id, testQuestionOptions)
        votosPoll1 = Poll.objects.get(id = testPoll.id)
        self.assertEqual(votosPoll1.votos_actuales, 1)
        
        insertVoteWeb(testPoll.id, testUser2.id, testQuestionOptions)
        votosPoll2 = Poll.objects.get(id = testPoll.id)
        self.assertEqual(votosPoll2.votos_actuales, 2)
        
        Vote.objects.all().delete()

    def testCheckOnlyOneVotePerUser(self):
        Vote.objects.all().delete()
        testPoll = Poll.objects.get(id = 1) 
        testPoll.startdate = datetime.datetime.strptime("2010-2-12", '%Y-%m-%d').date()
        testPoll.save()
               
        testUser = UserAccount.objects.get(id = 3)
        testQuestionOptions = "12&56"
        insertVoteWeb(testPoll.id, testUser.id, testQuestionOptions)
        self.assertRaises(MoreThanOneVoteException, checkOnlyOneVotePerUser, testPoll.id, testUser.id)
        Vote.objects.all().delete()
        
if __name__ == '__main__':
    unittest.main()    
    

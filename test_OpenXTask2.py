from OpenX_Task2 import *
import unittest

class TestOpenxTask2(unittest.TestCase):

    def test_who_is_the_closest_user_to_another(self):
        dict_of_latitude_and_longitude = get_latitude_and_longitude()
        #Those predicted user's ID should be correct, I checked it by calculations
        self.assertEqual(who_is_theclosest(1, dict_of_latitude_and_longitude,0)[0], 5)
        self.assertEqual(who_is_theclosest(4, dict_of_latitude_and_longitude,0)[0], 9)
        self.assertEqual(who_is_theclosest(8, dict_of_latitude_and_longitude,0)[0], 4)
        self.assertEqual(who_is_theclosest(10, dict_of_latitude_and_longitude,0)[0], 5)
        self.assertEqual(who_is_theclosest(6, dict_of_latitude_and_longitude,0)[0], 1)
    """
    Both tests for each solution should give the same outputs, which is True.
    Two functions give different result only in case where the ID of user is equal 6, 
    which is very interesting and i have no idea why is that. Checking distance on Google Maps
    the closest user for user 6 is user 10. Only in that case shapely library is wrong.
    
    """
    def test_who_is_the_closest_user_to_another_by_calculating_each(self):
        dict_of_latitude_and_longitude = get_latitude_and_longitude()
        self.assertEqual(getdistance(1, dict_of_latitude_and_longitude,0)[0], 5)
        self.assertEqual(getdistance(4, dict_of_latitude_and_longitude,0)[0], 9)
        self.assertEqual(getdistance(8, dict_of_latitude_and_longitude,0)[0], 4)
        self.assertEqual(getdistance(10, dict_of_latitude_and_longitude,0)[0], 5)
        self.assertEqual(getdistance(6, dict_of_latitude_and_longitude,0)[0], 10)

    def test_which_solution_is_faster(self):
        """
        Using get_time_from_each solution function we loop 30000 times over the same dictionary
        and find the same user over and over again. The point is to measure time for each function
        get_distance() and who_is_the_closest(). The results we can see below.
        Surprisingly method get_distance is faster than who_is_the_closest(), which I have to
        admit i did not expect.

        """
        time_of_to_solutuons = get_time_from_each_solution(1) #get time of finding the closest user for user 1
        who_is_the_closest_time = time_of_to_solutuons[0]
        get_distance_time = time_of_to_solutuons[1]
        self.assertGreater(who_is_the_closest_time,get_distance_time)

        time_of_to_solutuons = get_time_from_each_solution(1)
        who_is_the_closest_time2 = time_of_to_solutuons[0]
        get_distance_time2 = time_of_to_solutuons[1]
        self.assertGreater(who_is_the_closest_time2, get_distance_time2)

        time_of_to_solutuons = get_time_from_each_solution(1)
        who_is_the_closest_time3 = time_of_to_solutuons[0]
        get_distance_time3 = time_of_to_solutuons[1]
        self.assertGreater(who_is_the_closest_time3, get_distance_time3)



    def test_check_for_unique_titles(self):
        list_of_unique_titles = check_for_unique_titles()
        #in our case there was no unique titles so our list should be empty!
        self.assertEqual(list_of_unique_titles,[])

    def test_how_many_posts_did_users_add(self):
        list_of_strings = how_many()
        #let's check for example user number 5 which is Chelsey Dietrich
        self.assertEqual(list_of_strings[4], "Chelsey Dietrich added 10 posts")
        # let's check for example user number 2 which is Ervin Howell
        self.assertEqual(list_of_strings[1], "Ervin Howell added 10 posts")
        # let's check for example user number 8 which is Nicholas Runolfsdottir V
        self.assertEqual(list_of_strings[7], "Nicholas Runolfsdottir V added 10 posts")




if __name__ == '__main__':
    unittest.main()

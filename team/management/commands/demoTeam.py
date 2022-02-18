from django.core.management.base import BaseCommand, CommandError
from team.models import Librarian
from schools.models import School


class Command(BaseCommand):
    """Closes the specified poll for voting"""

    def handle(self, *args, **options):
        """"""
        school = School.objects.get(name="African Leadership Academy",
            town="Johannesburg",
            country="South Africa")
        resume = ['Emmanuel Murairi is experienced in software programming and web design. Driven by his willingness to solve problems in his community and transforming the world to a better place, he takes pride in providing the best solution possible. After implementing an automated grading system in a school back in his country, he started pursuing his leadership journey in African Leadership Academy (ALA) in South Africa. He is a Librarian in ALA, where his goals include providing a better learning experience to future African leaders of the academy. In addition, Emmanuel is the Director of Digital Media for ALAMAU 2020 where his works will contribute to solving pan African problems. Emmanuel is currently working on the African Libraries project which is a library management platform that aims to develop the reading culture within African youths. ',
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse proident, sunt in culpa qui officia deserunt mollit anim id est laborum.']
        usernames = ['Murairi', 'Takele', 'Etsehiwot']
        #names = ['Emmanuel Murairi', 'Emma Bizuneh Takele', 'Etsehiwot Teklu   Bekele']
        for i in range(3):     
            print(i)
            librarian = Librarian(username=usernames[i], school=school, profil=resume[i], role='Librarian')
        
            librarian.set_password(usernames[i])
            librarian.save()

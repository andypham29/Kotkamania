class FantasyPlayerGrader:

    @staticmethod
    def calculate_overall_grade(player_name, grade):
        grade_weighting = [10, 7, 3, 1]
        grade_weighting_no_grade = [9, 6, 1, 1]
        # grade_index = [1.025, 1, 1.0125,  0.93, 0.9]

        total_grade = 0
        total_weight = 0

        counter = 0

        for key in vars(grade):
            if vars(grade).get(key):
                total_grade += vars(grade).get(key) * grade_weighting[counter]
                total_weight += grade_weighting[counter]
            else:
                total_weight += grade_weighting_no_grade[counter]
            counter += 1

        print(
            f"20/21:{grade.current_year} "
            f"19/20:{grade.current_year_minus1} "
            f"18/19:{grade.current_year_minus2} "
            f"17/18:{grade.current_year_minus3} ")

        if total_weight == 0:
            return 0

        return round(total_grade / total_weight, 2)


class Grade:

    def __init__(self, current_year, current_year_minus1, current_year_minus2, current_year_minus3):
        self.current_year = current_year
        self.current_year_minus1 = current_year_minus1
        self.current_year_minus2 = current_year_minus2
        self.current_year_minus3 = current_year_minus3

import pandas as pd
from tests import scatter_solution_grades_of_maarih_around_the_general_mean, create_histograms_of_grades, \
    create_graph_of_academic_average_as_function_of_miun_grade, rank_grades_by_std_and_mean


"""
Main function : make some operations which filter the data and get specific columns
"""
def main(data_path):
    # manipulate the data
    data_frame = pd.read_excel(data_path)
    talpions = data_frame[data_frame["התקבל/לא התקבל"] == "התקבל"]  # take just talpions
    solution_rows_of_talpions = talpions[talpions["סוג מבחן"] == "solution"]  # take just solution rows
    solution_mesakem_grades = solution_rows_of_talpions.loc[:, "מסכם"].values  # get column of mesakem grades
    academic_grades = solution_rows_of_talpions.loc[:,"ממוצע אקדמי"].values
    talpions_group_by_maarihim = solution_rows_of_talpions.groupby(["מעריך"]).mean()
    average_mesakem_grades_given_by_maarih = talpions_group_by_maarihim.loc[:,"מסכם"].values
    maarihim_names = talpions_group_by_maarihim.axes[0].values

    # tests calls
    scatter_solution_grades_of_maarih_around_the_general_mean(solution_mesakem_grades, maarihim_names, average_mesakem_grades_given_by_maarih, solution_rows_of_talpions)
    create_histograms_of_grades(solution_mesakem_grades, maarihim_names, average_mesakem_grades_given_by_maarih)
    create_graph_of_academic_average_as_function_of_miun_grade(solution_mesakem_grades, academic_grades)
    rank_grades_by_std_and_mean(solution_mesakem_grades, maarihim_names, average_mesakem_grades_given_by_maarih)


if __name__ == "__main__":
    main(data_path="Data/data1.xlsx")

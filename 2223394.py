import pandas as pd

def run(path):
    df = pd.read_excel(path, sheet_name="Attendance_data")

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(['student_id', 'Date'])

    absences = df[df['Attendance_Status'] == 'Absent'].copy()
    absences['streak_group'] = absences.groupby('student_id')['Date'].diff().dt.days.ne(1).cumsum()

    streaks_df = absences.groupby(['student_id', 'streak_group']).agg(
        absence_start_date=('Date', 'first'),
        absence_end_date=('Date', 'last'),
        total_absent_days=('Date', 'count')
    ).reset_index().drop(columns=['streak_group'])

    return streaks_df

if __name__ == "__main__":
    file_path = input("Enter the path to the attendance file: ").strip('"')
    try:
        result = run(file_path)
        print(result.to_string(index=False))
    except Exception as e:
        print(f"Error: {e}")

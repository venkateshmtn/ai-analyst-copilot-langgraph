class CleaningAgent:

    def clean(self, df):

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Fill missing values
        df = df.fillna(0)

        return df
def build_schema_context(df):

    schema = []

    for col in df.columns:

        dtype = str(df[col].dtype)

        sample_values = (
            df[col]
            .dropna()
            .astype(str)
            .unique()[:3]
        )

        schema.append({
            "column": col,
            "dtype": dtype,
            "sample_values": list(sample_values)
        })

    return schema
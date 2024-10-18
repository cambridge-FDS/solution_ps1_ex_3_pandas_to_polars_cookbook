# %%
from numpy import dtype
import pandas as pd
import matplotlib.pyplot as plt
import polars as pl


DATA_PATH = "../data/311-service-requests.csv"
# %%
# We're going to use a new dataset here, to demonstrate how to deal with larger datasets. This is a subset of the of 311 service requests from [NYC Open Data](https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9).
# because of mixed types we specify dtype to prevent any errors
complaints = pd.read_csv(DATA_PATH, dtype="unicode")
complaints.head()

# %%
# TODO: rewrite the above using the polars library and call the data frame pl_complaints
# read everything in as strings (that's what we do with Pandas)
pl_complaints = pl.read_csv(DATA_PATH, infer_schema_length=0)
# see a discussion about dtype argument here: https://github.com/pola-rs/polars/issues/8230

# %%
# or read the error message: ComputeError: could not parse `NA` as dtype `i64` at column 'Incident Zip' (column number 9).
pl_complaints_na = pl.read_csv(DATA_PATH)

# %%
# we can handle "NA" explicitly
pl_complaints_na = pl.read_csv(DATA_PATH, null_values="NA")
# this throws another erro: ComputeError: could not parse `35209-3114` as dtype `i64` at column 'Incident Zip' (column number 9) -> the zip code gives us trouble because some zip codes have a dash.

# %%
# let's read this particular column as a string
pl_complaints_explicit = pl.read_csv(DATA_PATH, dtypes={"Incident Zip": pl.Utf8})

# %%
# Selecting columns:
complaints["Complaint Type"]

# %%
# TODO: rewrite the above using the polars library
pl_complaints.select(pl.col("Complaint Type"))
# %%
# Get the first 5 rows of a dataframe
complaints[:5]

# %%
# TODO: rewrite the above using the polars library
pl_complaints.head(5)
# %%
# Combine these to get the first 5 rows of a column:
complaints["Complaint Type"][:5]

# %%
# TODO: rewrite the above using the polars library
pl_complaints.select(pl.col("Complaint Type")).head(5)

# %%
# Selecting multiple columns
complaints[["Complaint Type", "Borough"]]

# %%
# TODO: rewrite the above using the polars library
pl_complaints.select([pl.col("Complaint Type"), pl.col("Borough")])

# or just:
pl_complaints.select(["Complaint Type", "Borough"])

# %%
# What's the most common complaint type?
complaint_counts = complaints["Complaint Type"].value_counts()
complaint_counts[:10]

# %%
# TODO: rewrite the above using the polars library
pl_most_complaints = (
    pl_complaints.select(pl.col("Complaint Type"))
    .to_series()  # I think not necessary
    .value_counts()
    .sort("count", descending=True)
    .head(10)  # This is already making it the top 10 df for plotting later
)

# %%
# Plot the top 10 most common complaints
complaint_counts[:10].plot(kind="bar")
plt.title("Top 10 Complaint Types")
plt.xlabel("Complaint Type")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# %%
# TODO: check if the code to plot the 10 most common complaints works also with your polars data frame
pl_most_complaints.plot.bar(x="Complaint Type", y="count")

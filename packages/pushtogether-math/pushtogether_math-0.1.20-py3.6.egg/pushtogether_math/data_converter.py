import pandas as pd


def populate_dataframe(dataframe, votes):
    """
    Populates Pandas DataFrame with the vote choices
    """
    for vote, user, comment in votes:
        dataframe.loc[user].loc[comment] = vote


def get_comments_set(votes):
    """
    Sort comments by ID
    """
    comments = sorted({comment for _, _, comment in votes})
    return comments


def get_users_set(votes):
    """
    Sort users by ID
    """
    users = sorted({user for _, user, _ in votes})
    return users


def convert_to_dataframe(votes):
    """
    Converts the votes stream in a Pandas DataFrame
    """
    comments = get_comments_set(votes)
    users = get_users_set(votes)
    votes_dataframe = pd.DataFrame(index=users, columns=comments)
    populate_dataframe(votes_dataframe, votes)
    return votes_dataframe.fillna(0)

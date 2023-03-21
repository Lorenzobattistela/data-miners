import os
import email
import logging
import pandas as pd
import numpy as np

SPAM = 0
HAM = 1



def email_dataset():
    ham_filenames = [name for name in sorted(os.listdir('./hamnspam/ham')) if len(name) > 20]
    spam_filenames = [name for name in sorted(os.listdir('./hamnspam/spam')) if len(name) > 20]

    ham_emails = [load_email(is_spam=False, filename=name) for name in ham_filenames]
    print(len(ham_emails))
    print(ham_emails[0])
    spam_emails = [load_email(is_spam=True, filename=name) for name in spam_filenames]
    print(len(spam_emails))
    print(ham_emails[0])
    
def load_email(is_spam: bool, filename: str):
    dir = "./hamnspam/spam" if is_spam else "./hamnspam/ham"
    try:
        with open(os.path.join(dir, filename), "rb") as f:
            return email.parser.BytesParser(policy=email.policy.default).parse(f)
    except IOError:
        logging.error(f"IoError: {IOError.with_traceback}")

def spam_dataset(filename: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filename, encoding="latin-1")
        logging.info("Loaded spam datasets successfully.")
    except FileNotFoundError:
        logging.error("File not found: %s", filename)
        exit()

    unnamed = [col for col in df.columns if col.startswith("Unnamed")]
    df.drop(columns=unnamed, inplace=True)
    df = df.rename(columns={"v1": "is_spam", "v2": "message"})
    df['is_spam'] = df['is_spam'].transform(lambda x: HAM if x == "ham" else SPAM)
    df.drop_duplicates(inplace=True)
    return df


def urls_dataset(filename: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print("File not found: {}".format(filename))
        exit()
    
    df['is_spam'] = df["is_spam"].transform(lambda x: SPAM if x == True else HAM)
    df.drop_duplicates(inplace=True)
    return df


def select_combinations(df: pd.DataFrame, combinations: int) -> pd.DataFrame:
    return df[df['is_spam'] == SPAM][:combinations].reset_index(drop=True).drop(columns='is_spam').to_numpy()


def combine_spam_messages_with_url(spam_df: pd.DataFrame, url_df: pd.DataFrame, combinations: int = 500) -> pd.DataFrame:
    spam_comb = select_combinations(spam_df, combinations)
    url_comb = select_combinations(url_df, combinations)

    spam_df = spam_df[~spam_df['message'].isin([msg for sublist in spam_comb for msg in sublist])]

    combined = []
    for msg, url in zip(spam_comb, url_comb):
        new_msg = msg[0] + f"\t{url[0]}"
        combined.append([new_msg])
    combined_df = pd.DataFrame(columns=['message'], data=combined)
    combined_df['is_spam'] = SPAM
    return pd.concat([spam_df, combined_df])


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    # spam_df = spam_dataset(filename='spam.csv')
    # url_df = urls_dataset('urls_spam.csv')
    # combined_df = combine_spam_messages_with_url(spam_df=spam_df, url_df=url_df)
    # logging.info("Combined dataframe with URLs to form new messages. New df shape: %s", combined_df.shape)
    email_dataset()


if __name__ == '__main__':
    main()
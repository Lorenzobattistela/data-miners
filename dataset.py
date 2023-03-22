import os
from email import parser, policy
import logging
import pandas as pd
import numpy as np

SPAM = 0
HAM = 1



def load_generated_spam() -> pd.DataFrame:
    try:
        df = pd.read_csv('generated_spam.csv', encoding="utf-8", delimiter='|')
        df['is_spam'] = df['is_spam'].transform(lambda x: SPAM if x == True else HAM)
        logging.info("Loaded generated spam dataset successfully.")
        return df
    except FileNotFoundError:
        logging.error("File not found: %s", 'generated_spam.csv')
        exit()

def email_dataset():
    ham_filenames = [name for name in sorted(os.listdir('./hamnspam/ham')) if len(name) > 20]
    spam_filenames = [name for name in sorted(os.listdir('./hamnspam/spam')) if len(name) > 20]

    ham_emails = [load_email(is_spam=False, filename=name) for name in ham_filenames]
    spam_emails = [load_email(is_spam=True, filename=name) for name in spam_filenames]

    spam_emails = [str(txt_email.get_payload()) for txt_email in spam_emails if get_email_structure(txt_email) == 'text/plain']
    ham_emails = [str(txt_email.get_payload()) for txt_email in ham_emails if get_email_structure(txt_email) == 'text/plain']
    email_df = pd.DataFrame(spam_emails, columns=['message'])
    email_df['is_spam'] = SPAM
    ham_df = pd.DataFrame(ham_emails, columns=['message'])
    ham_df['is_spam'] = HAM
    return pd.concat([email_df, ham_df])

def get_email_structure(email):
    if isinstance(email, str):
        return email
    payload = email.get_payload()
    if isinstance(payload, list):
        return "multipart({})".format(", ".join([
            get_email_structure(sub_email)
            for sub_email in payload
        ]))
    else:
        return email.get_content_type()

def load_email(is_spam: bool, filename: str):
    dir = "./hamnspam/spam" if is_spam else "./hamnspam/ham"
    try:
        with open(os.path.join(dir, filename), "rb") as f:
            return parser.BytesParser(policy=policy.default).parse(f)
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


def get_general_dataset() -> pd.DataFrame:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    spam_df = spam_dataset(filename='spam.csv')
    url_df = urls_dataset('urls_spam.csv')
    combined_df = combine_spam_messages_with_url(spam_df=spam_df, url_df=url_df)
    logging.info("Combined dataframe with URLs to form new messages. New df shape: %s", combined_df.shape)
    email_df = email_dataset()
    gen_spam_df = load_generated_spam()
    return pd.concat([combined_df, email_df, gen_spam_df])

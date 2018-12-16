import re
import pandas

enron_dataset_file_name = 'enron_email_dataset_sample.csv'


def main():
    with open(enron_dataset_file_name, 'rb') as f_in:
        raw_email_info = f_in.read()

        # Extract features we may potentially want to use (minus email body)
        dates = re.findall(r'\nDate: (.*)', raw_email_info)
        sender_addresses = re.findall(r'\nFrom: (.*)', raw_email_info)
        recipients = re.findall(r'\nTo: (.*)', raw_email_info)
        subjects = re.findall(r'\nSubject: (.*)', raw_email_info)
        sender_names = re.findall(r'\nX-From: (.*)', raw_email_info)
        recipient_names = re.findall(r'\nX-To: ([ A-Za-z]*)', raw_email_info)
        ccs = re.findall(r'\nX-cc: (.*)', raw_email_info)
        bccs = re.findall(r'\nX-bcc: (.*)', raw_email_info)
        folders = re.findall(r'"[a-zA-z-]*/(.*)/.*,"Message-ID.*>', raw_email_info)

        # Strip out all features to extract email body
        raw_email_info = re.sub(r'\nDate: (.*)', '', raw_email_info)
        raw_email_info = re.sub(r'\nFrom: (.*)', '', raw_email_info)
        raw_email_info = re.sub(r'\nTo: (.*)', '', raw_email_info)
        raw_email_info = re.sub(r'\nSubject: (.*)', '', raw_email_info)
        raw_email_info = re.sub(r'\nX-From: (.*)', '', raw_email_info)
        raw_email_info = re.sub(r'\nX-To: ([ A-Za-z]*)', '', raw_email_info)
        raw_email_info = re.sub(r'\nX-cc: (.*)', '', raw_email_info)
        raw_email_info = re.sub(r'\nX-bcc: (.*)', '', raw_email_info)
        raw_email_info = re.sub(r'\nX-Folder: (.*)', '', raw_email_info)

        raw_email_info = re.sub(r'"file","message"', '', raw_email_info)
        raw_email_info = re.sub(r'\nMime-Version: (.*)', '', raw_email_info)
        raw_email_info = re.sub(r'\nContent-Type: (.*)', '', raw_email_info)
        raw_email_info = re.sub(r'\nContent-Transfer-Encoding: (.*)', '', raw_email_info)
        raw_email_info = re.sub(r'\nX-Origin: (.*)', '', raw_email_info)
        raw_email_info = re.sub(r'\nX-FileName: (.*)', '', raw_email_info)
        raw_email_info = re.sub(r'".*Message-ID.*>', 'file_name_and_message_id', raw_email_info)

        bodies = [clean_email_body(body) for body in raw_email_info.split('file_name_and_message_id')[1:]]

        email_data = zip(dates,
                         sender_addresses,
                         recipients,
                         subjects,
                         sender_names,
                         recipient_names,
                         ccs,
                         bccs,
                         folders,
                         bodies)

        # Stick features into a dataframe to make it easy to query and filter out data
        df = pandas.DataFrame(email_data, columns=['date',
                                                   'sender_address',
                                                   'recipient',
                                                   'subject',
                                                   'sender_name',
                                                   'recipient_name',
                                                   'cc',
                                                   'bcc',
                                                   'folder',
                                                   'body'])

        # WIP: remove folders that are most likely computer generated
        new_df = df[
            (df.folder != '_sent_mail') &
            (df.folder != 'all_documents') &
            (df.folder != 'deleted_items') &
            (df.folder != 'inbox') &
            (df.folder != 'discussion_threads') &
            (df.folder != 'notes_inbox') &
            (df.folder != 'sent_items') &
            (df.folder != 'sent')
        ]

        print df.shape
        print new_df.shape


def clean_email_body(body):
    return body


if __name__ == '__main__':
    main()

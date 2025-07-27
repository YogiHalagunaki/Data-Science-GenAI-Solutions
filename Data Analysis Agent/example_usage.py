import pandas as pd
from data_cleaning_agent import DataCleaningAgent

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Create sample data
sample_data = {
    'location': [
        'United States', 
        'UK   ', 
        '  India', 
        'United States of America', 
        'Deutschland', 
        'u.s.a.',
        'USA',
        'united states',
        'N/A',
        '   ',
        'United Kingdom',
        'Great Britain',
        None
    ],
    'full_name': [
        'Yogi Halaguanki',
        'Vaishnavi Halagunaki',
        'DR. ROBERT BROWN',
        'Maria García',
        'Hans Schmidt',
        'j.doe  ',
        'ALICE WONDER',
        'bob wilson, jr.',
        'Mr. James O\'Connor',
        '???',
        None,
        '  ',
        'N/A'
    ],
    'email': [
        'Yogi.Halagunaki@email.com',
        'YOGI@COMPANY.COM',
        'invalid.email@',
        '@incomplete.com',
        'hans.schmidt@domain.de',
        'not_an_email',
        '',
        None,
        'multiple@@dots..com',
        'user@.com',
        'prefix@domain.c',
        'no@domain',
        'test@test.com'
    ],
    'phone': [
        '123-456-7890',
        '(555) 123-4567',
        '+1 234 567 8901',
        '12345',
        '++4499-1234-567',
        'NA',
        '000-000-0000',
        None,
        '123.456.7890',
        'invalid',
        '1234567890',
        '+44 7911 123456',
        ''
    ],
    'age': [
        25,
        30,
        150,
        35,
        40,
        -1,
        0,
        999,
        None,
        'unknown',
        '45',
        '',
        'N/A'
    ],
    'salary': [
        50000,
        60000.50,
        '55,000',
        1000000,
        65000,
        0,
        -10000,
        'undefined',
        None,
        '$75,000',
        '80K',
        'confidential',
        ''
    ],
    'date_joined': [
        '2023-01-01',
        '01/15/2023',
        '2023.02.01',
        'Jan 1, 2023',
        '20230401',
        'invalid date',
        None,
        '2023-13-45',
        'yesterday',
        '2023/05/01',
        '1st Jun 2023',
        '',
        '2023-06-31'
    ],
    'status': [
        'Active',
        'ACTIVE',
        'active',
        'Inactive',
        'Pending',
        'pending',
        'ON HOLD',
        None,
        '',
        'Unknown',
        'N/A',
        '1',
        'true'
    ]
}

df = pd.DataFrame(sample_data)

# Initialize the agent
agent = DataCleaningAgent()

# Clean the data
print("Starting data cleaning process...")
cleaned_df = agent.clean_data(df)

# Display results
print("\nOriginal Data:")
print(df)
print("\nCleaned Data:")
print(cleaned_df)

# Save the cleaned data
cleaned_df.to_csv("cleaned_data.csv", index=False)
print("\nCleaned data saved to 'cleaned_data.csv'") 
import os
import pycountry
import numpy as np
import pandas as pd
from scipy import stats
from fuzzywuzzy import fuzz
from dotenv import load_dotenv
from langgraph.graph import Graph
from typing import List, Dict, Any
from typing import TypedDict, Annotated

load_dotenv()

# Define state types
class AgentState(TypedDict):
    df: pd.DataFrame
    messages: List[str]
    column_types: Dict[str, List[str]]
    cleaned_df: pd.DataFrame

class DataCleaningAgent:
    def __init__(self):
        # Initialize country codes
        self.country_codes = {country.name: country.alpha_3 
                            for country in pycountry.countries}

    def print_response(self, message: str):
        """Print messages with formatting"""
        print(f"responce::::::::: {message}")

    def analyze_columns(self, state: AgentState) -> AgentState:
        """Analyze and classify columns in the dataset"""
        df = state['df']
        column_types = {
            'country': [],
            'address': [],
            'name': [],
            'numeric': []
        }
        
        for col in df.columns:
            # Check if column contains country names
            if any(word in col.lower() for word in ['country', 'nation', 'location']):
                column_types['country'].append(col)
                state['messages'].append(f"Identified country column: {col}")
            
            # Check if column contains addresses
            elif any(word in col.lower() for word in ['address', 'street']):
                column_types['address'].append(col)
                state['messages'].append(f"Identified address column: {col}")
            
            # Check if column contains names
            elif any(word in col.lower() for word in ['name', 'person']):
                column_types['name'].append(col)
                state['messages'].append(f"Identified name column: {col}")
            
            # Check if column is numeric
            elif pd.to_numeric(df[col], errors='coerce').notna().mean() > 0.8:
                column_types['numeric'].append(col)
                state['messages'].append(f"Identified numeric column: {col}")
        
        state['column_types'] = column_types
        return state

    def clean_countries(self, state: AgentState) -> AgentState:
        """Clean country columns"""
        df = state['cleaned_df']
        for col in state['column_types']['country']:
            df[f'{col}_normalized'] = df[col].apply(self._normalize_country)
            state['messages'].append(f"Normalized country names in column: {col}")
        state['cleaned_df'] = df
        return state

    def clean_addresses(self, state: AgentState) -> AgentState:
        """Clean address columns"""
        df = state['cleaned_df']
        for col in state['column_types']['address']:
            df[f'{col}_normalized'] = df[col].apply(self._normalize_address)
            state['messages'].append(f"Normalized addresses in column: {col}")
        state['cleaned_df'] = df
        return state

    def clean_names(self, state: AgentState) -> AgentState:
        """Clean name columns"""
        df = state['cleaned_df']
        for col in state['column_types']['name']:
            df[f'{col}_normalized'] = df[col].apply(self._normalize_name)
            state['messages'].append(f"Normalized names in column: {col}")
        state['cleaned_df'] = df
        return state

    def remove_numeric_outliers(self, state: AgentState) -> AgentState:
        """Remove outliers from numeric columns"""
        df = state['cleaned_df']
        for col in state['column_types']['numeric']:
            df[col] = self._remove_outliers(df[col])
            state['messages'].append(f"Removed outliers from column: {col}")
        state['cleaned_df'] = df
        return state

    def create_workflow(self) -> Graph:
        """Create the LangGraph workflow"""
        # Define the workflow
        workflow = Graph()

        # Add nodes
        workflow.add_node("analyze", self.analyze_columns)
        workflow.add_node("clean_countries", self.clean_countries)
        workflow.add_node("clean_addresses", self.clean_addresses)
        workflow.add_node("clean_names", self.clean_names)
        workflow.add_node("clean_numeric", self.remove_numeric_outliers)

        # Define edges with proper flow
        workflow.add_edge("analyze", "clean_countries")
        workflow.add_edge("clean_countries", "clean_addresses")
        workflow.add_edge("clean_addresses", "clean_names")
        workflow.add_edge("clean_names", "clean_numeric")

        # Set the entry point
        workflow.set_entry_point("analyze")

        # Compile the workflow
        return workflow.compile()

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean the provided dataframe using the workflow"""
        # Initialize state
        state: AgentState = {
            "df": df,
            "messages": [],
            "column_types": {},
            "cleaned_df": df.copy()
        }

        # Create and run workflow
        workflow = self.create_workflow()
        
        try:
            final_state = workflow.invoke(state)
            
            # Print messages
            for message in final_state["messages"]:
                self.print_response(message)
            
            return final_state["cleaned_df"]
        except Exception as e:
            print(f"Error during data cleaning: {str(e)}")
            return df  # Return original dataframe if cleaning fails

    def _normalize_country(self, country_name: str) -> str:
        """Normalize country names to ISO codes"""
        if pd.isna(country_name):
            return np.nan
        
        if country_name in self.country_codes:
            return self.country_codes[country_name]
        
        matches = [(name, fuzz.ratio(country_name.lower(), name.lower()))
                  for name in self.country_codes.keys()]
        best_match = max(matches, key=lambda x: x[1])
        
        if best_match[1] > 80:
            return self.country_codes[best_match[0]]
        return np.nan

    def _normalize_address(self, address: str) -> str:
        """Normalize address format"""
        if pd.isna(address):
            return np.nan
        
        address = str(address).strip().lower()
        replacements = {
            'st.': 'street',
            'rd.': 'road',
            'ave.': 'avenue',
            'blvd.': 'boulevard',
            'apt.': 'apartment'
        }
        for old, new in replacements.items():
            address = address.replace(old, new)
        return address.title()

    def _normalize_name(self, name: str) -> str:
        """Normalize name format"""
        if pd.isna(name):
            return np.nan
        
        name = str(name).strip().lower()
        name = ' '.join(name.split())
        return name.title()

    def _remove_outliers(self, series: pd.Series, threshold: float = 3) -> pd.Series:
        """Remove outliers using z-score method"""
        z_scores = np.abs(stats.zscore(series.dropna()))
        return series.mask(np.abs(stats.zscore(series.dropna())) > threshold)

    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from CSV or Excel file"""
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel files.")

    def save_data(self, df: pd.DataFrame, output_path: str):
        """Save cleaned data to CSV or Excel file"""
        if output_path.endswith('.csv'):
            df.to_csv(output_path, index=False)
        elif output_path.endswith(('.xlsx', '.xls')):
            df.to_excel(output_path, index=False)
        else:
            raise ValueError("Unsupported output format. Please use CSV or Excel files.") 
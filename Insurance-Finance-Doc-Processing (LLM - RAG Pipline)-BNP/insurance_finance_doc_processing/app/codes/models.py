from typing import List
from pydantic import BaseModel, Field
from datetime import date

class Trade(BaseModel):
    TradeID: int = Field(None, description="Unique identifier for the trade")
    ISIN: str = Field(None, description="International Securities Identification Number of the bond")
    Issuer: str = Field(None, description="Name of the issuing entity")
    Maturity: date = Field(None, description="Bond maturity date")
    Notional: float = Field(None, description="Total notional amount of the bond")
    Coupon: float = Field(None, description="Coupon rate of the bond in percentage")
    Currency: str = Field(None, description="Currency of denomination")
    SettlementDate: date = Field(None, description="Date on which settlement occurs")
    DayCountFraction: str = Field(None, description="Day count convention used (e.g., Actual/Actual)")
    InterestPaymentDate: date = Field(None, description="Next interest payment date")
    IssueDate: date = Field(None, description="Bond issuance date")
    IssueAmount: float = Field(None, description="Total issue size of the bond")
    IssuePrice: float = Field(None, description="Price at which the bond was issued (per unit)")
    NominalAmountPerBond: float = Field(None, description="Face value per bond unit")
    InterestPaymentFrequency: str = Field(None, description="Frequency of coupon payments (e.g., Annual)")
    BusinessDayConvention: str = Field(None, description="Convention used to adjust non-business days")
    BusinessDayLocation: List[str] = Field(None, description="Applicable financial centers for business day adjustment")
    AmortizationType: str = Field(None, description="Amortization type (e.g., Perpetual, Bullet, etc.)")
    MinimumSubscription: float = Field(None, description="Minimum subscription amount for investors")
    Parent: str = Field(None, description="Parent issuer organization")

class Trades(BaseModel):
    trades: List[Trade] = Field(..., description="List of trades with detailed bond information")

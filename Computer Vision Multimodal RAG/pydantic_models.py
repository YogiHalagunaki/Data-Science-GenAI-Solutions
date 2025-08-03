from typing import Optional
from pydantic import BaseModel, Field


class AssetDiscoveryTool(BaseModel):
    """
    An asset discovery tool is used to detect devices on the network. This is used for inventorying devices and detecting unauthorized devices.
    This control assesses:
        - Existence: The presence of an asset discovery tool.
        - Scope: The percentage of assets discoverable by the tool.
        - Other: The frequency of scans performed by the tool.
    """
    Existence: Optional[str] = Field("Not Provided", description="Existence of the asset discovery tool.")
    Scope: Optional[str] = Field("Not Provided", description="Percentage of assets covered by the discovery tool.")
    Other: Optional[str] = Field("Not Provided", description="Frequency of scans performed by the tool.")


class AuthorizedSoftware(BaseModel):
    """
    A list of authorized software is maintained by the organization to compare with a software inventory and identify unauthorized software.
    This control assesses:
        - Existence: Presence of a maintained list of authorized software.
        - Other: Reviewing, comparing, and removing unauthorized software.
    """
    Existence: Optional[str] = Field("Not Provided", description="Existence of the authorized software list.")
    Scope: Optional[str] = Field("Not Provided", description="Not applicable for this control.")
    Other: Optional[str] = Field("Not Provided", description="Actions taken to review and remove unauthorized software.")


class ConfigurationStandards(BaseModel):
    """
    Configuration standards are pre-defined guidelines for setting up and maintaining IT assets.
    This control assesses:
        - Existence: Presence of configuration standards across all asset types.
        - Other: Use of recognized frameworks and tools (e.g., SCCM, GPO) to manage these standards.
    """
    Existence: Optional[str] = Field("Not Provided", description="Existence of configuration standards.")
    Scope: Optional[str] = Field("Not Provided", description="Not applicable for this control.")
    Other: Optional[str] = Field("Not Provided", description="Usage of frameworks and tools for configuration standards.")


class CentralizedAccountManagement(BaseModel):
    """
    Centralized Account Management involves managing user accounts, permissions, and authentication across the organization using a unified system.
    This control assesses:
        - Existence: Presence of centralized account management practices.
        - Scope: The proportion of accounts managed centrally.
        - Other: The use of directory or identity services.
    """
    Existence: Optional[str] = Field("Not Provided", description="Existence of centralized account management.")
    Scope: Optional[str] = Field("Not Provided", description="Percentage of accounts managed centrally.")
    Other: Optional[str] = Field("Not Provided", description="Usage of directory or identity services.")


class PrivilegedAccessManagement(BaseModel):
    """
    Privileged Access Management (PAM) safeguards limit, monitor, and authenticate privileged account usage.
    This control assesses:
        - Existence: Presence of PAM capabilities.
        - Scope: Proportion of privileged accounts controlled by PAM capabilities.
        - Other: Usage of tools and advanced safeguards (e.g., password vaulting, session monitoring, MFA).
    """
    Existence: Optional[str] = Field("Not Provided", description="Existence of privileged access management capabilities.")
    Scope: Optional[str] = Field("Not Provided", description="Percentage of accounts managed with PAM capabilities.")
    Other: Optional[str] = Field("Not Provided", description="Usage of tools and safeguards for PAM.")


class CompromisedPasswordMonitoring(BaseModel):
    """
    Compromised Password Monitoring identifies breached credentials and enforces password resets.
    This control assesses:
        - Existence: Monitoring for compromised passwords.
        - Scope: Proportion of accounts monitored.
        - Other: Enforcement of password resets for breached credentials.
    """
    Existence: Optional[str] = Field("Not Provided", description="Existence of compromised password monitoring.")
    Scope: Optional[str] = Field("Not Provided", description="Percentage of accounts monitored.")
    Other: Optional[str] = Field("Not Provided", description="Enforcement of password resets for breached credentials.")


class MFA(BaseModel):
    """
    Multi-Factor Authentication (MFA) is a security mechanism requiring users to verify their identity using two or more factors.
    This control assesses:
        - Existence: Usage of MFA for specific scenarios.
        - Scope: Proportion of accounts or systems using MFA.
        - Other: Additional requirements or configurations for MFA.
    """
    Existence: Optional[str] = Field("Not Provided", description="Existence of MFA for the given scenario.")
    Scope: Optional[str] = Field("Not Provided", description="Percentage of accounts or systems using MFA.")
    Other: Optional[str] = Field("Not Provided", description="Additional configurations for MFA.")


class AccessControls(BaseModel):
    """
    Access Controls regulate who or what can view, use, or modify resources within a system.
    This control assesses:
        - Scope: System types where access controls are applied (e.g., databases, applications).
        - Other: Usage of role-based access controls and review frequency.
    """
    Existence: Optional[str] = Field("Not Provided", description="Existence of access controls.")
    Scope: Optional[str] = Field("Not Provided", description="System types where access controls are applied.")
    Other: Optional[str] = Field("Not Provided", description="Usage of role-based controls and review frequency.")


class DataLossPrevention(BaseModel):
    """
    Data Loss Prevention (DLP) detects and prevents unauthorized access or transfer of sensitive data.
    This control assesses:
        - Scope: Coverage of DLP tools across network, endpoints, and email.
        - Other: DLP tool configurations (e.g., blocking mode, data inventory updates).
    """
    Existence: Optional[str] = Field("Not Provided", description="Existence of DLP tooling.")
    Scope: Optional[str] = Field("Not Provided", description="Coverage of DLP tools across systems.")
    Other: Optional[str] = Field("Not Provided", description="Configuration and usage of DLP tools.")


class ControlEvaluations(BaseModel):
    """
    The parent model aggregates all control evaluations for streamlined assessment.
    """
    asset_discovery_tool: Optional[AssetDiscoveryTool] = Field(None, description="Asset Discovery Tool assessment.")
    authorized_software: Optional[AuthorizedSoftware] = Field(None, description="Authorized Software assessment.")
    configuration_standards: Optional[ConfigurationStandards] = Field(None, description="Configuration Standards assessment.")
    centralized_account_management: Optional[CentralizedAccountManagement] = Field(None, description="Centralized Account Management assessment.")
    privileged_access_management: Optional[PrivilegedAccessManagement] = Field(None, description="Privileged Access Management assessment.")
    compromised_password_monitoring: Optional[CompromisedPasswordMonitoring] = Field(None, description="Compromised Password Monitoring assessment.")
    mfa_external_platforms: Optional[MFA] = Field(None, description="MFA for External Platforms assessment.")
    mfa_remote_access: Optional[MFA] = Field(None, description="MFA for Remote Access assessment.")
    mfa_admin_accounts: Optional[MFA] = Field(None, description="MFA for Admin Accounts assessment.")
    access_controls: Optional[AccessControls] = Field(None, description="Access Controls assessment.")
    data_loss_prevention: Optional[DataLossPrevention] = Field(None, description="Data Loss Prevention assessment.")

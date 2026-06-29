"""
Salesforce Ecosystem registry — cloud definitions, MCP mappings, brain assignments.
"""

SF_CLOUDS = {
    "agentforce": {
        "name": "Agentforce",
        "icon": "🤖",
        "color": "#00A1E0",
        "desc": "AI agent platform — build, deploy, and monitor autonomous agents",
        "mcp_server": "agentforce-python",
        "key_features": ["Agent Builder", "Agent Testing", "Deployment", "Org Readiness"],
        "docs_url": "https://developer.salesforce.com/docs/einstein/einstein-agent-studio",
        "search_keywords": "salesforce agentforce AI agents autonomous",
        "folder": "agentforce",
    },
    "revenue-cloud": {
        "name": "Revenue Cloud / RLM",
        "icon": "💰",
        "color": "#2E844A",
        "desc": "Quote-to-cash, billing, subscriptions, pricing, contracts",
        "mcp_server": "salesforce-clouds-python",
        "key_features": ["CPQ", "Billing", "Subscriptions", "Revenue Lifecycle"],
        "docs_url": "https://help.salesforce.com/s/articleView?id=sf.revenue_lifecycle_management.htm",
        "search_keywords": "salesforce revenue cloud RLM CPQ billing subscription",
        "folder": "revenue-cloud",
    },
    "data-cloud": {
        "name": "Data Cloud",
        "icon": "🗄️",
        "color": "#8B5CF6",
        "desc": "Real-time customer data platform — unify, segment, activate",
        "mcp_server": "datacloud-python",
        "key_features": ["Data Ingestion", "Identity Resolution", "Segmentation", "Activation"],
        "docs_url": "https://developer.salesforce.com/docs/data/datahub",
        "search_keywords": "salesforce data cloud CDP customer data platform",
        "folder": "data-cloud",
    },
    "field-service": {
        "name": "Field Service",
        "icon": "🔧",
        "color": "#F59E0B",
        "desc": "Workforce management, scheduling, dispatch, mobile workers",
        "mcp_server": "servicecloud-fieldservice-python",
        "key_features": ["Scheduling", "Dispatch", "Mobile App", "Work Orders"],
        "docs_url": "https://help.salesforce.com/s/articleView?id=sf.field_service_intro.htm",
        "search_keywords": "salesforce field service FSL workforce management",
        "folder": "field-service",
    },
    "sales-cloud": {
        "name": "Sales Cloud",
        "icon": "📈",
        "color": "#0070D2",
        "desc": "CRM, leads, opportunities, forecasting, Einstein Sales AI",
        "mcp_server": "salesforce-clouds-python",
        "key_features": ["Opportunities", "Leads", "Forecasting", "Einstein AI"],
        "docs_url": "https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference",
        "search_keywords": "salesforce sales cloud CRM opportunities leads",
        "folder": "sales-cloud",
    },
    "service-cloud": {
        "name": "Service Cloud",
        "icon": "🎧",
        "color": "#00B5F1",
        "desc": "Case management, omni-channel, knowledge, Einstein bots",
        "mcp_server": "salesforce-clouds-python",
        "key_features": ["Cases", "Omni-Channel", "Knowledge", "Chat Bots"],
        "docs_url": "https://help.salesforce.com/s/articleView?id=sf.cases_overview.htm",
        "search_keywords": "salesforce service cloud customer support cases",
        "folder": "service-cloud",
    },
    "experience-cloud": {
        "name": "Experience Cloud",
        "icon": "🌐",
        "color": "#FF6B6B",
        "desc": "Portals, communities, digital experiences for customers/partners",
        "mcp_server": "salesforce-clouds-python",
        "key_features": ["Communities", "Portals", "LWR Sites", "Partner Hub"],
        "docs_url": "https://developer.salesforce.com/docs/component-library/documentation/en/lwc",
        "search_keywords": "salesforce experience cloud communities LWR portal",
        "folder": "experience-cloud",
    },
    "marketing-cloud": {
        "name": "Marketing Cloud",
        "icon": "📧",
        "color": "#F97316",
        "desc": "Email, journeys, personalization, advertising, analytics",
        "mcp_server": "marketingcloud-python",
        "key_features": ["Email Studio", "Journey Builder", "Personalization", "CDP"],
        "docs_url": "https://developer.salesforce.com/docs/marketing/marketing-cloud",
        "search_keywords": "salesforce marketing cloud email automation journey",
        "folder": "marketing-cloud",
    },
    "commerce-cloud": {
        "name": "Commerce Cloud",
        "icon": "🛒",
        "color": "#10B981",
        "desc": "B2B and B2C commerce, storefronts, order management",
        "mcp_server": "commerce-python",
        "key_features": ["B2B Commerce", "B2C Commerce", "Order Management", "Checkout"],
        "docs_url": "https://developer.salesforce.com/docs/commerce/salesforce-commerce",
        "search_keywords": "salesforce commerce cloud B2B B2C storefront",
        "folder": "commerce-cloud",
    },
    "omnistudio": {
        "name": "OmniStudio / Vlocity",
        "icon": "⚡",
        "color": "#6366F1",
        "desc": "Industry digital experiences — FlexCards, OmniScripts, DataRaptors",
        "mcp_server": "omnistudio-python",
        "key_features": ["FlexCards", "OmniScripts", "DataRaptors", "Integration Procedures"],
        "docs_url": "https://developer.salesforce.com/docs/industries/omnistudio",
        "search_keywords": "salesforce omnistudio vlocity flexcard omniscript",
        "folder": "omnistudio",
    },
    "loyalty": {
        "name": "Loyalty Management",
        "icon": "🏆",
        "color": "#EC4899",
        "desc": "Points, tiers, benefits, partner programs, redemption",
        "mcp_server": "loyalty-python",
        "key_features": ["Points Engine", "Tiers", "Benefits", "Partner Programs"],
        "docs_url": "https://help.salesforce.com/s/articleView?id=sf.loyalty_overview.htm",
        "search_keywords": "salesforce loyalty management points tiers rewards",
        "folder": "loyalty-cloud",
    },
    "industry-clouds": {
        "name": "Industry Clouds",
        "icon": "🏭",
        "color": "#84CC16",
        "desc": "Health, Financial Services, Manufacturing, Comms, Media",
        "mcp_server": "industry-clouds-python",
        "key_features": ["Health Cloud", "Financial Services", "Manufacturing", "Communications"],
        "docs_url": "https://developer.salesforce.com/docs/industries",
        "search_keywords": "salesforce industry clouds health financial manufacturing",
        "folder": "industry-clouds",
    },
}

BRAIN_SF_MAPPING = {
    "agentforce": {"primary": "claude", "secondary": "openai", "reason": "Agent design, spec generation, multi-turn"},
    "revenue-cloud": {"primary": "claude", "secondary": "deepseek", "reason": "Complex pricing logic, Apex code"},
    "data-cloud": {"primary": "openai", "secondary": "claude", "reason": "Data analysis, SQL, SOQL queries"},
    "field-service": {"primary": "claude", "secondary": "gemini", "reason": "Scheduling logic, workflow design"},
    "sales-cloud": {"primary": "claude", "secondary": "grok", "reason": "CRM strategy, real-time market context"},
    "service-cloud": {"primary": "claude", "secondary": "openai", "reason": "Case routing, knowledge generation"},
    "experience-cloud": {"primary": "claude", "secondary": "gemini", "reason": "LWC/LWR component code generation"},
    "marketing-cloud": {"primary": "gemini", "secondary": "claude", "reason": "Creative content, multi-modal campaigns"},
    "commerce-cloud": {"primary": "claude", "secondary": "deepseek", "reason": "Commerce logic, product catalog code"},
    "omnistudio": {"primary": "claude", "secondary": "deepseek", "reason": "FlexCard/OmniScript JSON/Apex"},
    "loyalty": {"primary": "claude", "secondary": "openai", "reason": "Points engine logic, tier rules"},
    "industry-clouds": {"primary": "claude", "secondary": "gemini", "reason": "Domain-specific healthcare/financial rules"},
}


def get_all_clouds() -> dict:
    return SF_CLOUDS


def get_cloud(cloud_id: str) -> dict | None:
    return SF_CLOUDS.get(cloud_id)


def get_brain_for_cloud(cloud_id: str) -> dict:
    return BRAIN_SF_MAPPING.get(cloud_id, {"primary": "claude", "secondary": "openai", "reason": "Default"})

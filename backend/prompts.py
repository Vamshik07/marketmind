def campaign_prompt(product, audience, platform):
    return f"""
You are a Chief Marketing Officer with expertise in creating data-driven marketing strategies.

Generate a comprehensive marketing campaign strategy with the following components:

1. Campaign Objectives - Clear, measurable goals for this campaign
2. Audience Psychology - Deep insights into the target audience's motivations and pain points
3. Content Ideas - 5 unique content ideas tailored to the platform
4. Ad Copy Variations - 3 compelling ad copy variations with different angles
5. Call-to-Action Strategy - Specific CTAs optimized for conversions on the platform

Product/Service: {product}
Target Audience: {audience}
Marketing Platform: {platform}

Please provide a detailed, actionable strategy that considers platform-specific best practices.
"""


def sales_prompt(product, persona):
    return f"""
You are a senior enterprise sales leader with experience in closing high-value deals.

Create a comprehensive sales pitch with the following components:

1. 30-Second Elevator Pitch - A concise, engaging pitch for initial contact
2. Value Proposition - Clear statement of business value and benefits
3. Key Differentiators - 4-5 key advantages versus competitive alternatives
4. Pain Point Alignment - How the solution addresses specific customer pain points
5. Closing Call-To-Action - Next steps to move the deal forward (demo, meeting, trial)

Product/Solution: {product}
Customer Persona: {persona}

Ensure the pitch is personalized, compelling, and focused on the customer's specific needs and situation.
"""


def lead_scoring_prompt(name, budget, need, urgency):
    return f"""
You are a sales intelligence analyst expert in lead qualification and scoring.

Evaluate this lead across multiple qualification dimensions and provide:

1. Lead Qualification Score (0-100) with clear scoring criteria:
   - 90-100: Hot leads (immediate follow-up)
   - 75-89: Warm leads (priority follow-up)
   - 60-74: Lukewarm leads (nurture)
   - Below 60: Cold leads (defer or disqualify)

2. Detailed Scoring Reasoning - Explain the score based on budget, need, urgency, and other factors

3. Probability of Conversion (%) - Estimated likelihood of deal closure

4. Sales Readiness Assessment - Is the lead ready to buy now?

5. Recommended Next Actions - Specific actions the sales team should take

Evaluate across these BANU dimensions:
- Budget: Available budget and spending authority
- Authority: Decision-making power and buying influence
- Need: Business pain points and solution fit
- Urgency: Timeline and implementation priority

Lead Information:
- Name: {name}
- Budget Information: {budget}
- Business Need: {need}
- Urgency Level: {urgency}

Provide a comprehensive qualification analysis that helps prioritize sales efforts.
"""

import datetime
from enum import Enum

class RiskTolerance(Enum):
    CONSERVATIVE = 1
    MODERATE = 2
    AGGRESSIVE = 3

class TimeHorizon(Enum):
    SHORT_TERM = 1  # 1-3 years
    MEDIUM_TERM = 2  # 3-7 years
    LONG_TERM = 3  # 7+ years

class InvestmentRecommender:
    def __init__(self):
        self.user_profile = {}
        
    def collect_user_info(self):
        """Collect user financial information and goals"""
        print("\n=== Investment Profile Questionnaire ===")
        
        # Basic financial information
        self.user_profile['age'] = int(input("Your age: "))
        self.user_profile['annual_income'] = float(input("Annual income ($): "))
        self.user_profile['savings'] = float(input("Current savings/investments ($): "))
        self.user_profile['debt'] = float(input("Total debt ($): "))
        
        # Risk tolerance
        print("\nRisk Tolerance:")
        print("1. Conservative (low risk)")
        print("2. Moderate (balanced risk/reward)")
        print("3. Aggressive (high risk for potential higher returns)")
        risk_choice = int(input("Select your risk tolerance (1-3): "))
        self.user_profile['risk_tolerance'] = RiskTolerance(risk_choice)
        
        # Time horizon
        print("\nInvestment Time Horizon:")
        print("1. Short-term (1-3 years)")
        print("2. Medium-term (3-7 years)")
        print("3. Long-term (7+ years)")
        horizon_choice = int(input("Select your time horizon (1-3): "))
        self.user_profile['time_horizon'] = TimeHorizon(horizon_choice)
        
        # Goals
        print("\nPrimary Investment Goals (select all that apply, comma separated):")
        print("1. Retirement")
        print("2. Buy a home")
        print("3. Education")
        print("4. Wealth building")
        print("5. Passive income")
        goal_choices = input("Enter goal numbers (e.g., 1,3,5): ")
        self.user_profile['goals'] = [int(g.strip()) for g in goal_choices.split(',')]
        
        # Special circumstances
        self.user_profile['has_emergency_fund'] = input("\nDo you have an emergency fund (3-6 months expenses)? (y/n): ").lower() == 'y'
        self.user_profile['has_retirement_account'] = input("Do you have a retirement account (401k/IRA)? (y/n): ").lower() == 'y'
    
    def analyze_financial_health(self):
        """Evaluate the user's financial foundation"""
        recommendations = []
        red_flags = []
        
        # Emergency fund check
        if not self.user_profile['has_emergency_fund']:
            recommendations.append("Build an emergency fund (3-6 months of expenses) before investing")
            red_flags.append("No emergency fund")
            
        # High debt check
        debt_to_income = self.user_profile['debt'] / self.user_profile['annual_income'] if self.user_profile['annual_income'] > 0 else 0
        if debt_to_income > 0.4:
            recommendations.append("Consider paying down high-interest debt before aggressive investing")
            red_flags.append(f"High debt-to-income ratio ({debt_to_income:.0%})")
            
        # Retirement account check
        if not self.user_profile['has_retirement_account'] and 1 in self.user_profile['goals']:
            recommendations.append("Open a retirement account (401k or IRA) for tax advantages")
            
        return recommendations, red_flags
    
    def generate_investment_recommendations(self):
        """Generate personalized investment recommendations"""
        recommendations = []
        
        # Start with financial health recommendations
        health_recs, red_flags = self.analyze_financial_health()
        recommendations.extend(health_recs)
        
        # Only proceed with investment recommendations if financial health is good
        if not red_flags or (len(red_flags) == 1 and "No emergency fund" in red_flags):
            # Asset allocation based on risk and time horizon
            allocation = self._get_asset_allocation()
            recommendations.append(f"\nSuggested Asset Allocation: {allocation}")
            
            # Account recommendations
            account_recs = self._get_account_recommendations()
            recommendations.extend(account_recs)
            
            # Strategy recommendations
            strategy_recs = self._get_strategy_recommendations()
            recommendations.extend(strategy_recs)
            
            # Additional tips based on goals
            goal_recs = self._get_goal_specific_recommendations()
            recommendations.extend(goal_recs)
            
        return recommendations
    
    def _get_asset_allocation(self):
        """Determine appropriate asset allocation mix"""
        risk = self.user_profile['risk_tolerance']
        horizon = self.user_profile['time_horizon']
        age = self.user_profile['age']
        
        # Base allocation based on risk tolerance
        if risk == RiskTolerance.CONSERVATIVE:
            stocks = 40 if horizon == TimeHorizon.LONG_TERM else 30
        elif risk == RiskTolerance.MODERATE:
            stocks = 60 if horizon == TimeHorizon.LONG_TERM else 50
        else:  # Aggressive
            stocks = 80 if horizon == TimeHorizon.LONG_TERM else 70
            
        # Adjust for age (more conservative as older)
        if age > 50:
            stocks -= 10
        elif age > 60:
            stocks -= 20
            
        bonds = 100 - stocks - 10  # Leave 10% for alternatives
        alternatives = 10
        
        return f"{stocks}% stocks, {bonds}% bonds, {alternatives}% alternatives (REITs, commodities)"
    
    def _get_account_recommendations(self):
        """Recommend account types based on situation"""
        recs = []
        goals = self.user_profile['goals']
        
        if 1 in goals:  # Retirement
            if self.user_profile['annual_income'] > 60000:
                recs.append("Maximize 401(k) contributions, especially if employer offers matching")
            recs.append("Consider opening a Roth IRA for tax-free growth (if income qualifies)")
            
        if 2 in goals:  # Buy a home
            if self.user_profile['time_horizon'] == TimeHorizon.MEDIUM_TERM:
                recs.append("For medium-term home purchase, consider a high-yield savings account or short-term bonds")
                
        if 3 in goals:  # Education
            recs.append("For education savings, consider a 529 plan for tax advantages")
            
        return recs
    
    def _get_strategy_recommendations(self):
        """Recommend investment strategies"""
        recs = []
        risk = self.user_profile['risk_tolerance']
        horizon = self.user_profile['time_horizon']
        
        recs.append("Diversify across different asset classes to manage risk")
        
        if risk == RiskTolerance.CONSERVATIVE:
            recs.append("Focus on index funds and ETFs for broad market exposure with low fees")
            recs.append("Consider dollar-cost averaging to reduce market timing risk")
        elif risk == RiskTolerance.MODERATE:
            recs.append("Mix of index funds and actively managed funds with strong track records")
            recs.append("Consider a core-satellite approach (core in index funds, satellite in select active funds)")
        else:  # Aggressive
            recs.append("Can allocate small portion (10-20%) to higher-risk opportunities")
            recs.append("Still maintain diversified core portfolio")
            
        if horizon == TimeHorizon.LONG_TERM:
            recs.append("With long time horizon, you can weather volatility - stay invested through downturns")
            
        return recs
    
    def _get_goal_specific_recommendations(self):
        """Additional recommendations based on specific goals"""
        recs = []
        goals = self.user_profile['goals']
        
        if 1 in goals:  # Retirement
            recs.append("\nFor retirement:")
            recs.append("- Aim to save 15% of income annually")
            recs.append("- Increase contributions by 1% each year until maxing out")
            recs.append("- Consider target-date funds for hands-off approach")
            
        if 4 in goals:  # Wealth building
            recs.append("\nFor wealth building:")
            recs.append("- Reinvest dividends for compound growth")
            recs.append("- Consider tax-efficient investments in taxable accounts")
            
        if 5 in goals:  # Passive income
            recs.append("\nFor passive income:")
            recs.append("- Look into dividend-paying stocks or funds")
            recs.append("- Consider real estate investment trusts (REITs)")
            
        return recs


def main():
    print("Investment Recommendation Engine")
    print("This tool will provide general investment guidance based on your profile.\n")
    
    recommender = InvestmentRecommender()
    recommender.collect_user_info()
    
    print("\n=== Analysis Results ===")
    
    # Show financial health check
    health_recs, red_flags = recommender.analyze_financial_health()
    if red_flags:
        print("\nFinancial Health Check:")
        for flag in red_flags:
            print(f"⚠️ {flag}")
    
    # Generate and display recommendations
    recommendations = recommender.generate_investment_recommendations()
    print("\nRecommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")
    
    print("\nRemember: These are general recommendations. Consider consulting with a financial advisor for personalized advice.")


if __name__ == "__main__":
    main()

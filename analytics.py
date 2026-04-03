"""
Analytics module for Seven Star Startup
Provides advanced metrics and insights
"""

import pandas as pd
from datetime import datetime, timedelta
from collections import Counter


class RepositoryAnalytics:
    """Analytics for repositories"""
    
    def __init__(self, repos_list):
        """Initialize with repository list"""
        self.repos = repos_list
        self.df = pd.DataFrame(repos_list) if repos_list else pd.DataFrame()
    
    def get_summary_stats(self):
        """Get basic summary statistics"""
        if self.df.empty:
            return {}
        
        return {
            'total_repos': len(self.repos),
            'unique_industries': self.df['industry'].nunique(),
            'avg_stars': float(self.df['stars'].mean()),
            'median_stars': float(self.df['stars'].median()),
            'max_stars': int(self.df['stars'].max()),
            'total_app_stars': int(self.df['app_stars'].sum()),
            'avg_rating': float(self.df['user_rating'].mean()) if 'user_rating' in self.df.columns else 0,
            'rated_count': int(self.df['user_rating'].notna().sum()) if 'user_rating' in self.df.columns else 0,
        }
    
    def get_industry_breakdown(self):
        """Get repositories by industry"""
        if self.df.empty:
            return {}
        
        industry_data = self.df.groupby('industry').agg({
            'id': 'count',
            'stars': ['mean', 'sum', 'max'],
            'app_stars': 'sum',
            'user_rating': 'mean'
        }).round(2)
        
        return industry_data.to_dict()
    
    def get_top_repos(self, metric='stars', limit=10):
        """Get top repositories by metric"""
        if self.df.empty:
            return []
        
        sorted_df = self.df.nlargest(limit, metric)
        return sorted_df[['name', 'industry', metric, 'user_rating']].to_dict('records')
    
    def get_trending_repos(self, limit=10):
        """Get trending repositories (by app_stars)"""
        return self.get_top_repos('app_stars', limit)
    
    def get_highly_rated(self, limit=10):
        """Get highly rated repositories"""
        if self.df.empty:
            return []
        
        rated_df = self.df.dropna(subset=['user_rating'])
        sorted_df = rated_df.nlargest(limit, 'user_rating')
        return sorted_df[['name', 'industry', 'user_rating', 'stars']].to_dict('records')
    
    def get_underrated_gems(self, min_stars=1000, limit=10):
        """Find underrated repos with high stars but low ratings"""
        if self.df.empty:
            return []
        
        gems = self.df[(self.df['stars'] >= min_stars) & (self.df['user_rating'].fillna(0) < 4)]
        sorted_df = gems.nlargest(limit, 'stars')
        return sorted_df[['name', 'industry', 'stars', 'user_rating']].to_dict('records')
    
    def get_growth_potential(self, limit=10):
        """Find repos with high star growth relative to ratings"""
        if self.df.empty:
            return []
        
        self.df['potential'] = self.df['stars'] / (self.df['user_rating'].fillna(1) + 1)
        sorted_df = self.df.nlargest(limit, 'potential')
        return sorted_df[['name', 'industry', 'stars', 'user_rating', 'potential']].to_dict('records')
    
    def get_distribution_stats(self):
        """Get distribution statistics"""
        if self.df.empty:
            return {}
        
        return {
            'stars': {
                'min': int(self.df['stars'].min()),
                'max': int(self.df['stars'].max()),
                'mean': float(self.df['stars'].mean()),
                'std': float(self.df['stars'].std()),
                'q1': float(self.df['stars'].quantile(0.25)),
                'q3': float(self.df['stars'].quantile(0.75)),
            },
            'rating': {
                'min': float(self.df['user_rating'].min()) if 'user_rating' in self.df.columns else 0,
                'max': float(self.df['user_rating'].max()) if 'user_rating' in self.df.columns else 0,
                'mean': float(self.df['user_rating'].mean()) if 'user_rating' in self.df.columns else 0,
            }
        }
    
    def get_source_distribution(self):
        """Get distribution by source"""
        if self.df.empty:
            return {}
        
        if 'source' in self.df.columns:
            return self.df['source'].value_counts().to_dict()
        return {}
    
    def get_health_score(self, repo_id):
        """Calculate health score for a repository (0-100)"""
        repo = next((r for r in self.repos if r.get('id') == repo_id), None)
        if not repo:
            return 0
        
        score = 0
        
        # Star score (0-30)
        max_stars = self.df['stars'].max() if not self.df.empty else 10000
        score += min(30, (repo.get('stars', 0) / max_stars * 30)) if max_stars > 0 else 0
        
        # Rating score (0-40)
        rating = repo.get('user_rating')
        score += (rating / 7 * 40) if rating else 0
        
        # Engagement score (0-20)
        app_stars = repo.get('app_stars', 0)
        max_app_stars = self.df['app_stars'].max() if not self.df.empty else 100
        score += min(20, (app_stars / max_app_stars * 20)) if max_app_stars > 0 else 0
        
        # Community score (0-10) - if user-submitted
        if repo.get('source') == 'user-submitted':
            score += 10
        
        return min(100, int(score))


class InvestmentAnalytics:
    """Analytics for investment decisions"""
    
    def __init__(self, repos_list, video_uploads=None):
        """Initialize with data"""
        self.repos = repos_list
        self.videos = video_uploads or []
        self.repo_analytics = RepositoryAnalytics(repos_list)
    
    def get_portfolio_score(self, rated_repos):
        """Calculate overall portfolio score"""
        if not rated_repos:
            return 0
        
        total_score = sum(r.get('user_rating', 0) for r in rated_repos if r.get('user_rating'))
        return round(total_score / len(rated_repos), 2) if rated_repos else 0
    
    def get_diversification_index(self, portfolio_repos):
        """Calculate portfolio diversification (0-100)"""
        if not portfolio_repos:
            return 0
        
        industries = [r.get('industry') for r in portfolio_repos]
        unique_industries = len(set(industries))
        total_industries = len(industries)
        
        diversity_score = (unique_industries / len(set(r.get('industry') for r in self.repos))) * 100 if self.repos else 0
        return min(100, int(diversity_score))
    
    def get_sector_opportunity_index(self):
        """Identify sectors with investment opportunity"""
        if not self.repos:
            return {}
        
        df = pd.DataFrame(self.repos)
        
        sector_analysis = {}
        for industry in df['industry'].unique():
            industry_repos = df[df['industry'] == industry]
            
            avg_stars = industry_repos['stars'].mean()
            avg_rating = industry_repos['user_rating'].mean()
            count = len(industry_repos)
            
            # Opportunity score: low rating with high stars = high opportunity
            opportunity = 100 - (avg_rating * 10 if not pd.isna(avg_rating) else 100)
            
            sector_analysis[industry] = {
                'count': count,
                'avg_stars': round(avg_stars, 0),
                'avg_rating': round(avg_rating, 2) if not pd.isna(avg_rating) else 0,
                'opportunity_score': round(opportunity, 0)
            }
        
        return sector_analysis
    
    def get_investment_recommendations(self):
        """Generate investment recommendations"""
        recommendations = []
        
        # Find underrated high-star projects
        gems = self.repo_analytics.get_underrated_gems()
        if gems:
            recommendations.append({
                'type': 'hidden_gems',
                'title': 'Hidden Gems: High Stars, Low Ratings',
                'description': 'Projects with strong GitHub presence but underrated on our platform',
                'count': len(gems),
                'action': 'Review and rate these projects'
            })
        
        # Find trending projects
        trending = self.repo_analytics.get_trending_repos(5)
        if trending:
            recommendations.append({
                'type': 'trending',
                'title': 'Platform Momentum',
                'description': 'Projects gaining traction from other investors',
                'count': len(trending),
                'action': 'See what others are investing in'
            })
        
        # Find growth potential
        growth = self.repo_analytics.get_growth_potential(5)
        if growth:
            recommendations.append({
                'type': 'growth',
                'title': 'High Growth Potential',
                'description': 'Projects with strong fundamentals and room to grow',
                'count': len(growth),
                'action': 'Consider for long-term investment'
            })
        
        return recommendations

class RepoAnalyzer:
    """Analyzes repositories and classifies them by industry."""

    INDUSTRIES = {
        'AI/ML': ['ai', 'ml', 'deep', 'neural', 'agent', 'llm', 'gpt', 'transformer', 'nlp'],
        'Media/Gaming': ['game', 'anime', 'toolkit', 'media', 'stream', 'video', 'audio', 'graphics'],
        'Cybersecurity': ['security', 'pentest', 'exploit', 'forensic', 'vuln', 'attack', 'defense'],
        'Cloud/DevOps': ['cloud', 'aws', 'server', 'infra', 'devops', 'k8s', 'kubernetes', 'docker'],
        'Education': ['education', 'learn', 'tutorial', 'course', 'book', 'lecture'],
        'Data Tools': ['data', 'db', 'dataset', 'warehouse', 'analytics', 'sql', 'nosql'],
        'Web/UI': ['web', 'ui', 'frontend', 'design', 'css', 'html', 'react', 'vue', 'angular'],
        'Mobile': ['mobile', 'android', 'ios', 'flutter', 'react-native', 'app'],
        'Finance': ['finance', 'payment', 'crypto', 'bitcoin', 'ethereum', 'trading'],
        'Infrastructure': ['infra', 'kubernetes', 'terraform', 'ansible', 'docker', 'compose']
    }

    def classify_industry(self, name, description):
        """Classify a project by industry based on name and description."""
        full_text = f"{name} {description}".lower()

        # Check each industry
        for industry, keywords in self.INDUSTRIES.items():
            if any(keyword in full_text for keyword in keywords):
                return industry

        return 'General Tech'

    def get_star_count_category(self, stars):
        """Categorize repositories by star count."""
        if stars < 100:
            return 'Emerging'
        elif stars < 1000:
            return 'Growing'
        elif stars < 10000:
            return 'Popular'
        else:
            return 'Mega-Popular'

    def calculate_investment_score(self, repo):
        """Calculate an investment score for a repository (0-100)."""
        score = 50  # Base score

        # Stars influence (max +30)
        stars = repo.get('stars', 0)
        if stars > 10000:
            score += 30
        elif stars > 5000:
            score += 20
        elif stars > 1000:
            score += 10

        # User rating influence (max +20)
        rating = repo.get('user_rating')
        if rating is not None:
            score += int((rating / 7) * 20)

        # App stars influence (max +10)
        app_stars = repo.get('app_stars', 0)
        score += min(app_stars, 10)

        # Portfolio adds (max +5)
        momentum = repo.get('app_stars', 0)
        if momentum > 50:
            score += 5

        return min(score, 100)

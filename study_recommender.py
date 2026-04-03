class StudyMaterialRecommender:
    """Recommends study materials for different project types and industries."""

    DOMAIN_RESOURCES = {
        'AI/ML': [
            'Official Project README & Documentation',
            'YouTube: "{name} tutorial" for hands-on walkthrough',
            'Deep Learning & ML Fundamentals via Coursera/fast.ai',
            'Research Papers via arXiv for theoretical foundation',
            'GitHub Awesome Lists for "{industry}" ecosystem overview'
        ],
        'Web/UI': [
            'Official Documentation & Code Examples',
            'YouTube: "{name} beginner" tutorial series',
            'Web Development Fundamentals - MDN Web Docs',
            'Design System & Component Documentation',
            'Community Showcase & Real-world Examples'
        ],
        'Cloud/DevOps': [
            'Official Platform Documentation',
            'YouTube: "{name} getting started" video',
            'Cloud Architecture Best Practices Course',
            'Infrastructure as Code Tutorials',
            'Community Blogs & Case Studies'
        ],
        'Data Tools': [
            'Official Getting Started Guide',
            'YouTube: "{name} tutorial for beginners"',
            'SQL/NoSQL Fundamentals Course',
            'Data Design Patterns & Best Practices',
            'Performance Tuning & Optimization Guides'
        ],
        'Cybersecurity': [
            'Official Security Guidelines & Best Practices',
            'YouTube: "{name} security testing demo"',
            'OWASP Top 10 & Security Fundamentals',
            'Penetration Testing Methodologies',
            'Real-world Vulnerability Case Studies'
        ],
        'General Tech': [
            'Official Project README & Contributing Guide',
            'Repository Discussions & Issues',
            'YouTube Search: "{name} overview and demo"',
            'Community Blog Posts & Articles',
            'GitHub Trending & Related Projects'
        ]
    }

    def get_materials(self, repo):
        """Get personalized study materials for a repository."""
        name = repo.get('name', repo.get('repo', 'this project'))
        industry = repo.get('industry', 'General Tech')

        # Get industry-specific resources
        materials = self.DOMAIN_RESOURCES.get(industry, self.DOMAIN_RESOURCES['General Tech'])

        # Format with repo name and industry
        formatted_materials = []
        for material in materials:
            formatted = material.format(name=name, industry=industry)
            formatted_materials.append(formatted)

        return formatted_materials

    def get_skill_path(self, industry):
        """Return a learning path for a specific industry."""
        paths = {
            'AI/ML': [
                '1. Python fundamentals & NumPy/Pandas',
                '2. Machine Learning basics & scikit-learn',
                '3. Deep Learning frameworks (PyTorch/TensorFlow)',
                '4. Large Language Models & Transformers',
                '5. Project implementation & deployment'
            ],
            'Web/UI': [
                '1. HTML/CSS/JavaScript fundamentals',
                '2. React/Vue/Angular framework',
                '3. Responsive design & accessibility',
                '4. State management & API integration',
                '5. Performance optimization & deployment'
            ],
            'Cloud/DevOps': [
                '1. Linux & command-line basics',
                '2. Docker & containerization',
                '3. Kubernetes orchestration',
                '4. CI/CD pipelines & automation',
                '5. Monitoring & infrastructure scaling'
            ],
            'Data Tools': [
                '1. SQL fundamentals & database design',
                '2. Data modeling & normalization',
                '3. Performance tuning & indexing',
                '4. Replication & backup strategies',
                '5. Data warehousing & analytics'
            ]
        }

        return paths.get(industry, ['1. Review documentation', '2. Follow tutorial', '3. Build project', '4. Contribute code', '5. Advance skills'])

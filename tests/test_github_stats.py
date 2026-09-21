import unittest
from unittest.mock import patch

from scripts import github_stats


class GitHubStatsTests(unittest.TestCase):
    def test_calculate_statistics_without_cache_uses_git_api_helper(self):
        with patch.object(github_stats, "_count_commits_for_repo", return_value=3), \
             patch.object(github_stats, "_get", return_value=[{
                 "author": {"login": "mohith-krishna-mahesh"},
                 "weeks": [
                     {"a": 10, "d": 2},
                     {"a": 20, "d": 1},
                 ],
             }]):
            stats = github_stats.calculate_statistics(
                {"public_repos": 1, "followers": 4},
                [{"name": "demo-repo"}],
                use_cache=False,
            )

            self.assertEqual(stats["commits"], 3)
            self.assertEqual(stats["additions"], 30)
            self.assertEqual(stats["deletions"], 3)
            self.assertEqual(stats["total_loc"], 27)


if __name__ == "__main__":
    unittest.main()

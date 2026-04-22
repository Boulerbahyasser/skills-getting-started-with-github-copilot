"""Test suite for Mergington High School Activities API endpoints
Using the Arrange-Act-Assert (AAA) pattern for test structure
"""

import pytest
from src import app as app_module


class TestRootEndpoint:
    """Tests for the GET / root endpoint"""

    def test_root_redirect(self, client):
        """Test that GET / redirects to /static/index.html
        
        Arrange: Client is ready
        Act: Make GET request to root endpoint
        Assert: Verify 307 redirect status and location header
        """
        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestActivitiesEndpoint:
    """Tests for the GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns the full activities dictionary
        
        Arrange: Client is ready
        Act: Make GET request to retrieve activities
        Assert: Verify response contains all expected activities with correct structure
        """
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        
        # Verify all activities are present
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Soccer Club",
            "Art Club",
            "Drama Club",
            "Debate Club",
            "Science Club"
        ]
        for activity_name in expected_activities:
            assert activity_name in activities
        
        # Verify activity structure
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint"""

    def test_signup_for_activity_success(self, client, monkeypatch):
        """Test successful registration of a new student for an activity
        
        Arrange: Mock activities with test data, new student email
        Act: Make POST request to signup endpoint
        Assert: Verify student is added to participants and success message returned
        """
        # Arrange
        test_activities = {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu"]
            }
        }
        monkeypatch.setattr(app_module, "activities", test_activities)
        
        new_student_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/Chess Club/signup",
            params={"email": new_student_email}
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert new_student_email in result["message"]
        assert new_student_email in test_activities["Chess Club"]["participants"]


class TestUnregisterEndpoint:
    """Tests for the DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_from_activity_success(self, client, monkeypatch):
        """Test successful unregistration of a student from an activity
        
        Arrange: Mock activities with test data including a student to remove
        Act: Make DELETE request to unregister endpoint
        Assert: Verify student is removed from participants and success message returned
        """
        # Arrange
        student_email = "michael@mergington.edu"
        test_activities = {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": [student_email, "daniel@mergington.edu"]
            }
        }
        monkeypatch.setattr(app_module, "activities", test_activities)
        
        # Act
        response = client.delete(
            f"/activities/Chess Club/unregister",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert student_email in result["message"]
        assert student_email not in test_activities["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in test_activities["Chess Club"]["participants"]

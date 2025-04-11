import pytest
from unittest.mock import patch, MagicMock
from marshmallow import ValidationError
from datetime import datetime, timezone
from src.campaigns.services import CampaignService
from src.campaigns.models import Campaign


class TestCampaignServiceUnit:

    @patch("src.campaigns.services.db_session")
    @patch("src.campaigns.services.Campaign")
    @patch("src.campaigns.services.CampaignSchema")
    def test_create_campaign_success(self, mock_schema, mock_campaign_class, mock_db_session):
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session

        mock_start_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        mock_end_date = datetime(2023, 1, 10, tzinfo=timezone.utc)

        mock_validated_data = {
            "name": "Test Campaign",
            "description": "Test",
            "start_date": mock_start_date,
            "end_date": mock_end_date,
            "budget": 1000.0,
            "is_active": True
        }
        mock_schema_instance = MagicMock()
        mock_schema.return_value = mock_schema_instance
        mock_schema_instance.load.return_value = mock_validated_data

        mock_campaign = MagicMock()
        mock_campaign.name = "Test Campaign"
        mock_campaign.description = "Test"
        mock_campaign.owner_id = 1
        mock_owner = MagicMock()
        mock_campaign.owner = mock_owner
        mock_campaign_class.return_value = mock_campaign

        def refresh_side_effect(obj):
            return obj

        mock_session.refresh.side_effect = refresh_side_effect

        test_data = {
            "name": "Test Campaign",
            "description": "Test",
            "start_date": mock_start_date,
            "end_date": mock_end_date,
            "budget": 1000.0,
            "is_active": True
        }
        owner_id = 1

        result = CampaignService.create_campaign(test_data, owner_id)

        mock_schema_instance.load.assert_called_once_with(test_data)
        mock_session.add.assert_called_once_with(mock_campaign)
        mock_session.commit.assert_called_once()

        assert mock_session.refresh.call_count == 2
        calls = [call[0][0] for call in mock_session.refresh.call_args_list]
        assert mock_campaign in calls
        assert mock_owner in calls

        assert result.name == mock_campaign.name
        assert result.description == mock_campaign.description
        assert result.owner_id == owner_id

    @patch("src.campaigns.services.db_session")
    @patch("src.campaigns.services.CampaignSchema")
    def test_create_campaign_validation_error(self, mock_schema, mock_db_session):
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session

        mock_schema_instance = MagicMock()
        mock_schema.return_value = mock_schema_instance
        mock_schema_instance.load.side_effect = ValidationError("Invalid data")

        test_data = {"invalid": "data"}
        owner_id = 1

        with pytest.raises(ValueError, match="Validation failed"):
            CampaignService.create_campaign(test_data, owner_id)

        mock_session.rollback.assert_called_once()

    @patch("src.campaigns.services.db_session")
    @patch("src.campaigns.services.get_jwt_identity")
    def test_get_user_campaign_success(self, mock_jwt, mock_db_session):
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session

        mock_jwt.return_value = 1
        mock_campaign = MagicMock()

        mock_query = mock_session.query.return_value
        mock_query.options.return_value.filter.return_value.first.return_value = mock_campaign

        campaign_id = 1

        result = CampaignService.get_campaign(campaign_id)

        mock_jwt.assert_called_once()
        assert result == mock_campaign

    @patch("src.campaigns.services.db_session")
    @patch("src.campaigns.services.get_jwt_identity")
    def test_get_user_campaign_not_found(self, mock_jwt, mock_db_session):
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session

        mock_jwt.return_value = 1
        mock_session.query.return_value.options.return_value.filter.return_value.first.return_value = None

        campaign_id = 1

        with pytest.raises(ValueError, match="Campaign not found or access denied"):
            CampaignService.get_campaign(campaign_id)

    @patch("src.campaigns.services.db_session")
    @patch("src.campaigns.services.get_jwt_identity")
    @patch("src.campaigns.services.CampaignUpdateSchema")
    def test_update_campaign_success(self, mock_schema, mock_jwt, mock_db_session):
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session

        mock_jwt.return_value = 1
        mock_campaign = MagicMock()
        mock_campaign.start_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        mock_campaign.end_date = datetime(2023, 1, 10, tzinfo=timezone.utc)
        mock_session.query.return_value.options.return_value.filter.return_value.first.return_value = mock_campaign

        mock_validated_data = {"name": "Updated Name"}
        mock_schema_instance = MagicMock()
        mock_schema.return_value = mock_schema_instance
        mock_schema_instance.load.return_value = mock_validated_data

        campaign_id = 1
        update_data = {"name": "Updated Name"}

        result = CampaignService.update_campaign(campaign_id, update_data)

        mock_schema_instance.load.assert_called_once_with(update_data, partial=True)
        assert mock_campaign.name == "Updated Name"
        mock_session.commit.assert_called_once()
        assert result == mock_campaign

    @patch("src.campaigns.services.db_session")
    @patch("src.campaigns.services.get_jwt_identity")
    def test_delete_campaign_success(self, mock_jwt, mock_db_session):
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session

        mock_jwt.return_value = 1
        mock_campaign = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_campaign

        campaign_id = 1

        result = CampaignService.delete_campaign(campaign_id)

        mock_session.delete.assert_called_once_with(mock_campaign)
        mock_session.commit.assert_called_once()
        assert result is True

    @patch("src.campaigns.services.db_session")
    @patch("src.campaigns.services.get_jwt_identity")
    def test_delete_campaign_not_found(self, mock_jwt, mock_db_session):
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session

        mock_jwt.return_value = 1
        mock_session.query.return_value.filter.return_value.first.return_value = None

        campaign_id = 1

        with pytest.raises(ValueError, match="Campaign not found or access denied"):
            CampaignService.delete_campaign(campaign_id)

    @patch("src.campaigns.services.db_session")
    @patch("src.campaigns.services.get_jwt_identity", return_value=1)
    def test_get_user_campaigns_success(self, mock_jwt, mock_db_session):
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session

        mock_campaigns = [MagicMock(), MagicMock()]
        mock_session.query.return_value.filter.return_value.all.return_value = mock_campaigns

        result = CampaignService.get_user_campaigns()

        mock_session.query.assert_called_once_with(Campaign)
        mock_session.query.return_value.filter.assert_called_once()
        mock_session.query.return_value.filter.return_value.all.assert_called_once()
        assert result == mock_campaigns

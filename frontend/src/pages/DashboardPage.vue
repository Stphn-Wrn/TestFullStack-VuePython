<template>
  <v-container>
    <v-app-bar color="primary" dense>
      <v-toolbar-title>Dashboard</v-toolbar-title>
      <v-spacer />
      <v-btn
        variant="outlined"
        data-cy="open-create-dialog"
        @click="openCampaignDialog"
      >
        Create a campaign
      </v-btn>
      <v-btn
        variant="outlined"
        color="black"
        class="ml-2 disconnect"
        data-cy="logout-btn"
        @click="handleLogout"
      >
        Disconnect
      </v-btn>
    </v-app-bar>

    <v-row>
      <v-col
        v-if="!campaignStore.isLoading && campaigns.length === 0"
        cols="12"
      >
        <v-alert type="info" border="left" colored-border>
          No campaigns found. Click on "Create a campaign" to get started.
        </v-alert>
      </v-col>

      <v-col
        v-for="(campaign, index) in campaigns"
        :key="index"
        cols="12"
        md="4"
      >
        <v-card>
          <v-card-title :data-cy="`campaign-title-${campaign.name}`">{{
            campaign.name
          }}</v-card-title>
          <v-card-subtitle>{{ campaign.description }}</v-card-subtitle>
          <v-card-text>
            <p>
              <strong>Start date:</strong> {{ formatDate(campaign.start_date) }}
            </p>
            <p>
              <strong>End date:</strong> {{ formatDate(campaign.end_date) }}
            </p>
            <p><strong>Budget:</strong> {{ campaign.budget }}€</p>
            <p>
              <strong>Status:</strong>
              <v-chip :color="campaign.is_active ? 'green' : 'red'">
                {{ campaign.is_active ? 'Active' : 'Inactive' }}
              </v-chip>
            </p>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="blue"
              data-cy="view-campaign-btn"
              @click="viewCampaign(campaign)"
            >
              See More
            </v-btn>
            <v-btn
              color="red"
              data-cy="delete-campaign-btn"
              @click="askDeleteCampaign(index)"
            >
              Delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>{{
          isEditing ? 'Edit Campaign' : 'Campaign Details'
        }}</v-card-title>

        <v-card-text>
          <v-alert
            v-if="updateErrors.length"
            type="error"
            class="mb-4"
            dense
            border="start"
          >
            <ul class="pl-4 no-bullets">
              <li v-for="(err, index) in updateErrors" :key="index">
                {{ err }}
              </li>
            </ul>
          </v-alert>
          <v-text-field
            v-model="modalCampaign.name"
            label="Campaign Name"
            :disabled="!isEditing"
            data-cy="edit-name"
          />
          <v-textarea
            v-model="modalCampaign.description"
            label="Description"
            :disabled="!isEditing"
            auto-grow
            data-cy="edit-description"
          />

          <v-date-input
            v-model="modalCampaign.start_date"
            label="Start date"
            :disabled="!isEditing"
            data-cy="edit-start"
          ></v-date-input>
          <v-date-input
            v-model="modalCampaign.end_date"
            label="End date"
            :disabled="!isEditing"
            data-cy="edit-end"
          ></v-date-input>

          <v-text-field
            v-model="modalCampaign.budget"
            label="Budget"
            type="number"
            data-cy="edit-budget"
            :disabled="!isEditing"
          />
          <v-select
            v-model="modalCampaign.is_active"
            label="Status"
            data-cy="edit-status"
            :items="[
              { text: 'Active', value: true },
              { text: 'Inactive', value: false },
            ]"
            item-title="text"
            item-value="value"
            :disabled="!isEditing"
          />
        </v-card-text>

        <v-card-actions>
          <v-btn
            color="red"
            @click="isEditing ? cancelEdit() : (dialog = false)"
          >
            {{ isEditing ? 'Cancel Edit' : 'Close' }}
          </v-btn>

          <v-btn
            color="primary"
            data-cy="edit-save"
            @click="isEditing ? saveCampaign() : toggleEditMode()"
          >
            {{ isEditing ? 'Save Changes' : 'Edit' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="createDialog" max-width="500">
      <v-card>
        <v-card-title>Create a Campaign</v-card-title>

        <v-card-text>
          <v-alert
            v-if="formErrors.length"
            type="error"
            class="mb-4"
            dense
            border="start"
          >
            <ul class="pl-4 no-bullets">
              <li v-for="(error, index) in formErrors" :key="index">
                {{ error }}
              </li>
            </ul>
          </v-alert>
          <v-text-field
            v-model="newCampaign.name"
            label="Campaign Name"
            required
            data-cy="create-name"
          />
          <v-textarea
            v-model="newCampaign.description"
            label="Description"
            data-cy="create-description"
          />
          <v-date-input
            v-model="newCampaign.start_date"
            label="Start date"
            data-cy="create-start"
          ></v-date-input>
          <v-date-input
            v-model="newCampaign.end_date"
            label="End date"
            data-cy="create-end"
          ></v-date-input>

          <v-text-field
            v-model="newCampaign.budget"
            label="Budget"
            type="number"
            data-cy="create-budget"
          />
          <v-select
            v-model="newCampaign.is_active"
            label="Status"
            data-cy="create-status"
            :items="[
              { text: 'Active', value: true },
              { text: 'Inactive', value: false },
            ]"
            item-title="text"
            item-value="value"
          />
        </v-card-text>

        <v-card-actions>
          <v-btn color="grey" @click="createDialog = false"> Cancel </v-btn>
          <v-btn
            color="primary"
            data-cy="create-submit"
            @click="submitCreateCampaign"
          >
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Confirm Deletion</v-card-title>
        <v-card-text>
          Are you sure you want to delete this campaign ? This action cannot be
          undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="cancelDelete"
            >Cancel</v-btn
          >
          <v-btn color="red" variant="flat" @click="confirmDeleteCampaign"
            >Delete</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="showSnackbar" timeout="3000" color="info">
      {{ toastMessage }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useCampaignStore } from '@/stores/campaignStore';
import { useAuthStore } from '@/stores/authStore';

const router = useRouter();
const authStore = useAuthStore();
const campaignStore = useCampaignStore();

const dialog = ref(false);
const createDialog = ref(false);
const isEditing = ref(false);
const formErrors = ref([]);
const updateErrors = ref([]);
const modalCampaign = ref({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  budget: '',
  is_active: 'Active',
});
const newCampaign = ref({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  budget: '',
  is_active: 'Active',
});
const campaigns = computed(() => campaignStore.campaigns);
const confirmDeleteDialog = ref(false);
const campaignToDelete = ref(null);
const toastMessage = ref('');
const showSnackbar = ref(false);

const showToast = (message) => {
  toastMessage.value = message;
  showSnackbar.value = true;
};

const askDeleteCampaign = (index) => {
  campaignToDelete.value = index;
  confirmDeleteDialog.value = true;
};

const cancelDelete = () => {
  confirmDeleteDialog.value = false;
  campaignToDelete.value = null;
};

const formatDate = (dateStr) => {
  return dateStr ? dateStr.slice(0, 10) : '';
};
const isEmpty = (field) => {
  return !field || String(field).trim() === '';
};

const openCampaignDialog = () => {
  newCampaign.value = {
    name: '',
    description: '',
    start_date: '',
    end_date: '',
    budget: '',
    is_active: 'Active',
  };

  createDialog.value = true;
  formErrors.value = [];
};

const submitCreateCampaign = async () => {
  const form = newCampaign.value;
  formErrors.value = [];

  if (
    isEmpty(form.name) ||
    isEmpty(form.description) ||
    isEmpty(form.start_date) ||
    isEmpty(form.end_date) ||
    isEmpty(form.budget)
  ) {
    formErrors.value.push('All fields must be filled out.');
  }

  if (form.start_date && form.end_date) {
    const start = new Date(form.start_date);
    const end = new Date(form.end_date);
    if (start >= end) {
      formErrors.value.push(
        'The start date must be earlier than the end date.',
      );
    }
  }

  if (formErrors.value.length > 0) return;

  const payload = {
    name: form.name,
    description: form.description,
    start_date: new Date(form.start_date).toISOString(),
    end_date: new Date(form.end_date).toISOString(),
    budget: parseInt(form.budget),
    is_active: form.is_active === true || form.is_active === 'Active',
  };

  await campaignStore.createCampaign(payload);
  createDialog.value = false;
  await fetchCampaigns();
};

const fetchCampaigns = async () => {
  await campaignStore.fetchCampaigns();
  campaigns.value = campaignStore.campaigns;
};

onMounted(() => {
  fetchCampaigns();
});
const backupCampaign = ref({});

const viewCampaign = (campaign) => {
  modalCampaign.value = {
    ...campaign,
    start_date: formatDate(campaign.start_date),
    end_date: formatDate(campaign.end_date),
  };
  backupCampaign.value = { ...modalCampaign.value };
  isEditing.value = false;
  dialog.value = true;
};

const toggleEditMode = () => {
  isEditing.value = true;
  console.log('isEditing (toggleEditMode):', isEditing.value);
};

const saveCampaign = async () => {
  if (!isEditing.value) return;

  updateErrors.value = [];

  const requiredFields = [
    'name',
    'description',
    'start_date',
    'end_date',
    'budget',
  ];
  requiredFields.forEach((field) => {
    const value = modalCampaign.value[field];
    if (!value && value !== 0) {
      updateErrors.value.push(`Le champ "${field}" est obligatoire.`);
    }
  });

  if (modalCampaign.value.start_date && modalCampaign.value.end_date) {
    const startDate = new Date(modalCampaign.value.start_date);
    const endDate = new Date(modalCampaign.value.end_date);

    if (startDate >= endDate) {
      updateErrors.value.push(
        'La date de fin doit être après la date de début.',
      );
    }
  }

  if (updateErrors.value.length > 0) {
    showToast('Veuillez corriger les erreurs dans le formulaire.');
    return;
  }

  const payload = {
    name: modalCampaign.value.name,
    description: modalCampaign.value.description,
    start_date: new Date(modalCampaign.value.start_date).toISOString(),
    end_date: new Date(modalCampaign.value.end_date).toISOString(),
    budget: Number(modalCampaign.value.budget),
    is_active: modalCampaign.value.is_active,
  };

  try {
    const result = await campaignStore.updateCampaign(
      modalCampaign.value.id,
      payload,
    );

    if (result.success) {
      showToast(result.message || 'Campagne mise à jour avec succès !');
      await fetchCampaigns();
      dialog.value = false;
      isEditing.value = false;
    } else {
      showToast(result.message || 'Erreur lors de la mise à jour');
    }
  } catch (error) {
    console.error('Erreur lors de la sauvegarde :', error);
    showToast(error.message || 'Une erreur inattendue est survenue');
  } finally {
    isEditing.value = false;
  }
};

const cancelEdit = () => {
  isEditing.value = false;
  modalCampaign.value = { ...backupCampaign.value };
};

const confirmDeleteCampaign = async () => {
  if (campaignToDelete.value !== null) {
    await campaignStore.deleteCampaign(
      campaigns.value[campaignToDelete.value].id,
    );
    await fetchCampaigns();
    confirmDeleteDialog.value = false;
    campaignToDelete.value = null;
  }
};

const handleLogout = async () => {
  await authStore.logout();
  router.push('/');
};
</script>

<style scoped>
.v-container {
  padding-top: 80px !important;
  height: auto;
}

.no-bullets {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.v-card {
  transition: 0.3s;
}
.v-card:hover {
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}

.dashboard-content {
  padding-top: 64px;
  height: auto;
  display: flex;
  flex-direction: column;
}

.v-main {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.disconnect {
  margin-inline-end: 20px !important;
}

.error-style .v-field {
  border: 1px solid #f44336 !important;
  border-radius: 4px;
}
</style>

<template>
  <v-container>
    <v-app-bar color="primary" dense>
      <v-toolbar-title>Dashboard</v-toolbar-title>
      <v-spacer />
      <v-btn variant="outlined" @click="openCampaignDialog">
        Create a campaign
      </v-btn>
      <v-btn
        variant="outlined"
        color="black"
        class="ml-2 disconnect"
        
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
          <v-card-title>{{ campaign.name }}</v-card-title>
          <v-card-subtitle>{{ campaign.description }}</v-card-subtitle>
          <v-card-text>
            <p><strong>Start date:</strong> {{ formatDate(campaign.start_date) }}</p>
            <p><strong>End date:</strong> {{ formatDate(campaign.end_date) }}</p>
            <p><strong>Budget:</strong> {{ campaign.budget }}€</p>
            <p>
              <strong>Status:</strong>
              <v-chip :color="campaign.status ? 'green' : 'red'">
                {{ campaign.status ? 'Actif' : 'Inactif' }}
              </v-chip>
            </p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="blue" @click="viewCampaign(campaign)">
              See More
            </v-btn>
            <v-btn color="red" @click="askDeleteCampaign(index)"> Delete </v-btn>
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
              <li v-for="(err, index) in updateErrors" :key="index">{{ err }}</li>
            </ul>
          </v-alert>
          <v-text-field v-model="modalCampaign.name" label="Campaign Name" :disabled="!isEditing"/>
          <v-textarea v-model="modalCampaign.description" label="Description" :disabled="!isEditing" auto-grow/>
          
          <v-date-input v-model="modalCampaign.start_date" label="Start date" :disabled="!isEditing"></v-date-input>
          <v-date-input v-model="modalCampaign.end_date" label="End date" :disabled="!isEditing"></v-date-input>
          
          <v-text-field
            v-model="modalCampaign.budget"
            label="Budget"
            type="number"
            :disabled="!isEditing"
          />
          <v-select
            v-model="modalCampaign.status"
            label="Status"
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
          />
          <v-textarea 
          v-model="newCampaign.description" 
          label="Description"

          />
          <v-date-input v-model="newCampaign.start_date" label="Start date"></v-date-input>
          <v-date-input v-model="newCampaign.end_date" label="End date"></v-date-input>
          
          <v-text-field
            v-model="newCampaign.budget"
            label="Budget"
            type="number"

          />
          <v-select
            v-model="newCampaign.status"
            label="Status"
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
          <v-btn color="primary" @click="submitCreateCampaign"> Create </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>

  <v-dialog v-model="confirmDeleteDialog" max-width="400">
  <v-card>
    <v-card-title class="text-h6">Confirm Deletion</v-card-title>
    <v-card-text>
      Are you sure you want to delete this campaign ? This action cannot be undone.
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="grey" variant="text" @click="cancelDelete">Cancel</v-btn>
      <v-btn color="red" variant="flat" @click="confirmDeleteCampaign">Delete</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
<v-snackbar v-model="showSnackbar" timeout="3000" color="info">
  {{ toastMessage }}
</v-snackbar>

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
const submitted = ref(false);
const formErrors = ref([]);
const updateErrors = ref([]);
const modalCampaign = ref({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  budget: '',
  status: 'Active',
});
const newCampaign = ref({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  budget: '',
  status: 'Active',
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
    status: 'Active',
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
      formErrors.value.push('The start date must be earlier than the end date.');
    }
  }

  if (formErrors.value.length > 0) return;

  const payload = {
    name: form.name,
    description: form.description,
    start_date: new Date(form.start_date).toISOString(),
    end_date: new Date(form.end_date).toISOString(),
    budget: parseInt(form.budget),
    status: form.status === true || form.status === 'Active',
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

  const allowedFields = ['name', 'description', 'start_date', 'end_date', 'budget', 'status'];
  const payload = {};

  allowedFields.forEach((field) => {
    if (modalCampaign.value[field] !== backupCampaign.value[field]) {
      payload[field] = modalCampaign.value[field];
    }
  });


  const requiredFields = ['name', 'description', 'start_date', 'end_date', 'budget'];
  requiredFields.forEach((field) => {
    const value = payload[field] !== undefined ? payload[field] : modalCampaign.value[field];
    if (!String(value).trim()) {
      updateErrors.value.push(`The "${field}" field cannot be empty.`);
    }
  });

  const start = payload.start_date || modalCampaign.value.start_date;
  const end = payload.end_date || modalCampaign.value.end_date;

  if (start && end) {
    const startDate = new Date(start);
    const endDate = new Date(end);
    if (startDate >= endDate) {
      updateErrors.value.push('The start date must be earlier than the end date.');
    }
  }

  if (updateErrors.value.length > 0) return;

  if (Object.keys(payload).length === 0) {
    showToast('No changes detected.');
    dialog.value = false;
    isEditing.value = false;
    return;
  }

  const result = await campaignStore.updateCampaign(modalCampaign.value.id, payload);

  showToast(result.message);
  dialog.value = false;
  isEditing.value = false;
  await fetchCampaigns();
};


const cancelEdit = () => {
  isEditing.value = false;
  modalCampaign.value = { ...backupCampaign.value };
};

const confirmDeleteCampaign = async () => {
  if (campaignToDelete.value !== null) {
    await campaignStore.deleteCampaign(campaigns.value[campaignToDelete.value].id);
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

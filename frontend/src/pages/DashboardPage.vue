<template>
  <v-container>
    <v-app-bar color="primary" dense>
      <v-toolbar-title>Dashboard</v-toolbar-title>
      <v-spacer></v-spacer>
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
      

      <v-col cols="12" v-if="!campaignStore.isLoading && campaigns.length === 0">
        <v-alert type="info" border="left" colored-border>
          No campaigns found. Click on "Create a campaign" to get started.
        </v-alert>
      </v-col>

      <v-col cols="12" md="4" v-for="(campaign, index) in campaigns" :key="index">
        <v-card>
          <v-card-title>{{ campaign.name }}</v-card-title>
          <v-card-subtitle>{{ campaign.description }}</v-card-subtitle>
          <v-card-text>
            <p><strong>Start date:</strong> {{ campaign.startDate }}</p>
            <p><strong>End date:</strong> {{ campaign.endDate }}</p>
            <p><strong>Budget:</strong> {{ campaign.budget }}€</p>
            <p><strong>Status:</strong> <v-chip :color="campaign.status ? 'green' : 'red'">{{ campaign.status ? 'Actif' : 'Inactif' }}</v-chip></p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="blue" @click="viewCampaign(campaign)">See More</v-btn>
            <v-btn color="red" @click="deleteCampaign(index)">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>{{ isEditing ? 'Edit Campaign' : 'Campaign Details' }}</v-card-title>

        <v-card-text>
          <v-text-field v-model="modalCampaign.name" label="Campaign Name" />
          <v-textarea v-model="modalCampaign.description" label="Description" />
          <v-text-field v-model="modalCampaign.startDate" label="Start Date" type="date" />
          <v-text-field v-model="modalCampaign.endDate" label="End Date" type="date" />
          <v-text-field v-model="modalCampaign.budget" label="Budget" type="number" />
          <v-select
            v-model="modalCampaign.status"
            label="Status"
            :items="[
              { text: 'Active', value: true },
              { text: 'Inactive', value: false }
            ]"
            item-title="text"
            item-value="value"
          />
        </v-card-text>

        <v-card-actions>
          <v-btn color="red" @click="isEditing ? cancelEdit() : dialog = false">
            {{ isEditing ? 'Cancel Edit' : 'Close' }}
          </v-btn>

          <v-btn color="primary" @click="isEditing ? saveCampaign() : toggleEditMode()">
            {{ isEditing ? 'Save Changes' : 'Edit' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="createDialog" max-width="500">
      <v-card>
        <v-card-title>Create a Campaign</v-card-title>

        <v-card-text>
          <v-text-field v-model="newCampaign.name" label="Campaign Name" required></v-text-field>
          <v-textarea v-model="newCampaign.description" label="Description"></v-textarea>
          <v-text-field v-model="newCampaign.startDate" label="Start Date" type="date"></v-text-field>
          <v-text-field v-model="newCampaign.endDate" label="End Date" type="date"></v-text-field>
          <v-text-field v-model="newCampaign.budget" label="Budget" type="number"></v-text-field>
          <v-select
            v-model="newCampaign.status"
            label="Status"
            :items="[
              { text: 'Active', value: true },
              { text: 'Inactive', value: false }
            ]"
            item-title="text"
            item-value="value"
          />
        </v-card-text>

        <v-card-actions>
          <v-btn color="grey" @click="createDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="submitCreateCampaign">Create</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
const createDialog = ref(false)
const isEditing = ref(false);
const modalCampaign = ref({
  name: '',
  description: '',
  startDate: '',
  endDate: '',
  budget: '',
  status: 'Active'
});
const newCampaign = ref({
  name: '',
  description: '',
  startDate: '',
  endDate: '',
  budget: '',
  status: 'Active'
})
const campaigns = computed(() => campaignStore.campaigns);

onMounted(() => {
  campaignStore.fetchCampaigns();
});

const openCampaignDialog = () => {
  newCampaign.value = {
    name: '',
    description: '',
    startDate: '',
    endDate: '',
    budget: '',
    status: 'Active'
  }
  createDialog.value = true
}

const submitCreateCampaign = async () => {
  const form = newCampaign.value;

  const payload = {
    name: form.name,
    description: form.description,
    start_date: new Date(form.startDate).toISOString(),
    end_date: new Date(form.endDate).toISOString(),
    budget: parseInt(form.budget),
    status: form.status === true || form.status === 'Active'
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
  modalCampaign.value = { ...campaign }
  backupCampaign.value = { ...campaign }
  isEditing.value = false
  dialog.value = true
};

const toggleEditMode = () => {
  isEditing.value = true;
  console.log('isEditing (toggleEditMode):', isEditing.value); 
};

const saveCampaign = async () => {
  if (isEditing.value) {
    await campaignStore.updateCampaign(modalCampaign.value.id, modalCampaign.value)
  }

  dialog.value = false
  isEditing.value = false
  await fetchCampaigns()
}


const cancelEdit = () => {
  isEditing.value = false;
  modalCampaign.value = { ...backupCampaign.value };
};


const deleteCampaign = async (index) => {
  await campaignStore.deleteCampaign(campaigns.value[index].id);
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

</style>

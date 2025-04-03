<template>
    <v-container>
      <v-toolbar>
        <v-toolbar-title>Tableau de Bord</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="createCampaign">Créer une campagne</v-btn>
      </v-toolbar>
      
      <v-list>
        <v-list-item v-for="(campaign, index) in campaigns" :key="index">
          <v-list-item-title>{{ campaign.name }}</v-list-item-title>
          <v-list-item-subtitle>{{ campaign.description }}</v-list-item-subtitle>
          <v-btn icon="mdi-pencil" @click="editCampaign(index)"></v-btn>
          <v-btn icon="mdi-delete" color="red" @click="deleteCampaign(index)"></v-btn>
        </v-list-item>
      </v-list>
    </v-container>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const campaigns = ref([
    { name: 'Campagne 1', description: 'Description de la campagne 1' },
    { name: 'Campagne 2', description: 'Description de la campagne 2' }
  ]);
  
  const createCampaign = () => {
    console.log('Créer une nouvelle campagne');
  };
  
  const editCampaign = (index) => {
    console.log('Modifier la campagne', campaigns.value[index]);
  };
  
  const deleteCampaign = (index) => {
    campaigns.value.splice(index, 1);
  };
  </script>
  
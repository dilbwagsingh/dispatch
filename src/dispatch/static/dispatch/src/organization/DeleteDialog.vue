<template>
  <v-dialog v-model="showRemove" persistent max-width="800px">
    <v-card>
      <v-card-title>
        <span class="headline">Delete Organization?</span>
      </v-card-title>
      <!--<v-alert
        :value="alert"
        type="error"
        transition="slide-y-transition"
      >There was an issue deleting.</v-alert>-->
      <v-card-text>
        <v-container grid-list-md>
          <v-layout wrap> Are you sure you would like to delete this organization? </v-layout>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="blue en-1" text @click="closeRemove()"> Cancel </v-btn>
        <v-btn color="red en-1" text @click="remove()"> Delete </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from "vuex"
import { mapFields } from "vuex-map-fields"
export default {
  name: "OrganizationDeleteDialog",
  data() {
    return {}
  },
  computed: {
    ...mapFields("organization", ["dialogs.showRemove"]),
  },

  methods: {
    ...mapActions("organization", ["remove", "closeRemove"]),
  },
}
</script>

<template>
  <ValidationObserver v-slot="{ invalid, validated }">
    <v-navigation-drawer v-model="showCreateEdit" app clipped right width="500">
      <template v-slot:prepend>
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title v-if="id" class="title"> Edit </v-list-item-title>
            <v-list-item-title v-else class="title"> New </v-list-item-title>
            <v-list-item-subtitle>Team</v-list-item-subtitle>
          </v-list-item-content>
          <v-btn
            icon
            color="info"
            :loading="loading"
            :disabled="invalid || !validated"
            @click="save()"
          >
            <v-icon>save</v-icon>
          </v-btn>
          <v-btn icon color="secondary" @click="closeCreateEdit()">
            <v-icon>close</v-icon>
          </v-btn>
        </v-list-item>
      </template>
      <v-card flat>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <span class="subtitle-2">Details</span>
              </v-flex>
              <v-flex xs12>
                <ValidationProvider name="Name" rules="required" immediate>
                  <v-text-field
                    v-model="name"
                    slot-scope="{ errors, valid }"
                    :error-messages="errors"
                    :success="valid"
                    label="Name"
                    hint="A name for your organization."
                    clearable
                    required
                  />
                </ValidationProvider>
              </v-flex>
              <v-flex xs12>
                <ValidationProvider name="Email" rules="required" immediate>
                  <v-text-field
                    v-model="email"
                    slot-scope="{ errors, valid }"
                    label="Email"
                    :error-messages="errors"
                    :success="valid"
                    hint="The organization's email."
                    clearable
                    required
                  />
                </ValidationProvider>
              </v-flex>
              <v-flex xs12>
                <ValidationProvider name="Company" rules="required" immediate>
                  <v-text-field
                    v-model="company"
                    slot-scope="{ errors, valid }"
                    label="Company"
                    :error-messages="errors"
                    :success="valid"
                    hint="The organization's company."
                    clearable
                    required
                  />
                </ValidationProvider>
              </v-flex>
              <v-flex xs12>
                <span class="subtitle-2">Engagement</span>
              </v-flex>
              <v-flex xs12>
                <term-combobox v-model="terms" />
              </v-flex>
              <v-flex xs12>
                <incident-priority-multi-select v-model="incident_priorities" />
              </v-flex>
              <v-flex>
                <incident-type-multi-select v-model="incident_types" :visibilities="visibilities" />
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
      </v-card>
    </v-navigation-drawer>
  </ValidationObserver>
</template>

<script>
import { mapFields } from "vuex-map-fields"
import { mapActions } from "vuex"
import { ValidationObserver, ValidationProvider, extend } from "vee-validate"
import { required } from "vee-validate/dist/rules"
import IncidentPriorityMultiSelect from "@/incident_priority/IncidentPriorityMultiSelect.vue"
import IncidentTypeMultiSelect from "@/incident_type/IncidentTypeMultiSelect.vue"
import TermCombobox from "@/term/TermCombobox.vue"

extend("required", {
  ...required,
  message: "This field is required",
})

export default {
  name: "ServiceNewEditSheet",

  data() {
    return {
      visibilities: ["Open"],
    }
  },

  components: {
    ValidationObserver,
    ValidationProvider,
    IncidentPriorityMultiSelect,
    IncidentTypeMultiSelect,
    TermCombobox,
  },

  computed: {
    ...mapFields("organization", [
      "selected.name",
      "selected.terms",
      "selected.company",
      "selected.email",
      "selected.incident_priorities",
      "selected.incident_types",
      "selected.id",
      "selected.loading",
      "dialogs.showCreateEdit",
    ]),
  },

  methods: {
    ...mapActions("organization", ["save", "closeCreateEdit"]),
  },
}
</script>

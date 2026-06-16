<script setup>

    import { ref, computed } from 'vue'
    import { useRoute } from 'vue-router'

    import PageLayout from '@/layout/PageLayout.vue'

    import Sidebar from '@/layout/Sidebar.vue';
    import Bottombar from '@/layout/Bottombar.vue';
    import Topbar from '@/layout/Topbar.vue';

    import { getSections, getActiveComponent } from '@/config/sections.js'

    const route = useRoute()
    const sections = getSections(route.path)

    const activeSection = ref(sections[0].id)
    const activeComponent = computed(() => getActiveComponent(sections, activeSection.value))

    const scenes = ['Noche', 'Mañana', 'Cine', 'Todo off']
    const activeScene = ref('Noche')

    function selectScene(name) {
        activeScene.value = name
    }

</script>

<template>

    <PageLayout>

        <Sidebar v-model:activeSection="activeSection" />

        <main class="flex flex-col flex-1">
            <Topbar :activeSection="activeSection" />

            <!-- Scenes row — mobile only -->
            <div v-if="activeSection === 'blueprint'" class="md:hidden px-5 pt-2 pb-1 shrink-0">
                <div class="scenes-row">
                    <button
                        v-for="scene in scenes"
                        :key="scene"
                        @click="selectScene(scene)"
                        class="scene-pill"
                        :class="{ active: activeScene === scene }"
                    >
                        {{ scene }}
                    </button>
                </div>
            </div>

            <component :is="activeComponent" />
        </main>

        <Bottombar v-model:activeSection="activeSection" />

    </PageLayout>

</template>

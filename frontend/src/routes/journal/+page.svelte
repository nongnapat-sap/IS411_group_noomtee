<script>
    import { enhance } from '$app/forms';
    
    let { data = {}, form = null } = $props();
    let myLogs = $derived(data?.logs || []);
    let places = $derived(data?.places || []);

    // State ควบคุม Modal
    let isModalOpen = $state(false);
    let isEditMode = $state(false);
    let formData = $state({ id: '', place_id: '', title: '', rating: 5, note: '' });

    function openAddModal() {
        isEditMode = false;
        formData = { id: '', place_id: '', title: '', rating: 5, note: '' };
        isModalOpen = true;
    }

    function openEditModal(log) {
        isEditMode = true;
        formData = { id: log.id, place_id: log.place_id, title: log.title, rating: log.rating, note: log.note };
        isModalOpen = true;
    }

    function closeModal() {
        isModalOpen = false;
    }
</script>

<div class="mt-5 mb-6">
    <p class="is-size-7 has-text-weight-bold mb-1" style="color: #ccff00;">MY DIARY</p>
    <h1 class="title is-2 has-text-white mb-2">Journal</h1>
    <p class="has-text-grey">Journal of your experiences and reviews</p>
</div>

{#if form?.message}
    <div class="notification is-danger is-light">{form.message}</div>
{/if}

<div class="box mb-6" style="background-color: #1a1a1a; border: 1px dashed #333;">
    <p class="has-text-weight-bold mb-3" style="color: #ccff00;">+ Log a new experience</p>
    <button onclick={openAddModal} class="button is-small has-text-weight-bold" style="background-color: #ccff00; color: black;">
        Add Review
    </button>
</div>

<h2 class="title is-4 has-text-white mb-4">Recent Logs</h2>
<div class="columns is-multiline">
    {#each myLogs as log (log.id)}
        <div class="column is-6">
            <div class="card" style="background-color: #1a1a1a; border-radius: 12px; height: 100%;">
                <div class="card-content">
                    <div class="is-flex is-justify-content-space-between is-align-items-center mb-2">
                        <p class="title is-5 has-text-white mb-0">{log.title}</p>
                    </div>
                    
                    <p class="mb-3 is-size-6">{'⭐'.repeat(log.rating || 5)}</p>
                    <p class="content has-text-grey-light is-size-7" style="font-style: italic;">"{log.note}"</p>
                    
                    <div class="buttons mt-4">
                        <button onclick={() => openEditModal(log)} class="button is-small is-dark">Edit</button>
                        <form method="POST" action="?/delete" use:enhance>
                            <input type="hidden" name="id" value={log.id} />
                            <button type="submit" class="button is-small is-danger is-outlined">Delete</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    {:else}
        <p class="column has-text-grey">You haven't logged any experiences yet.</p>
    {/each}
</div>

<!-- Modal Form -->
{#if isModalOpen}
    <div class="modal is-active">
        <div class="modal-background" onclick={closeModal} role="button" tabindex="0" onkeypress={closeModal}></div>
        <div class="modal-card">
            <header class="modal-card-head" style="background-color: #1a1a1a; border-bottom: 1px solid #333;">
                <p class="modal-card-title has-text-white">{isEditMode ? 'Edit Review' : 'Add New Review'}</p>
                <button class="delete" aria-label="close" onclick={closeModal}></button>
            </header>
            
            <section class="modal-card-body" style="background-color: #222;">
                <form method="POST" action={isEditMode ? '?/update' : '?/create'} use:enhance={() => {
                    return async ({ update }) => {
                        await update();
                        closeModal();
                    };
                }}>
                    {#if isEditMode}
                        <input type="hidden" name="id" value={formData.id} />
                    {/if}

                    <div class="field">
                        <label class="label has-text-grey-light">Place</label>
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="place_id" bind:value={formData.place_id} required style="background-color: #111; color: white; border-color: #444;">
                                    <option value="" disabled>Select a place...</option>
                                    {#each places as place}
                                        <option value={place.place_id}>{place.place_name}</option>
                                    {/each}
                                </select>
                            </div>
                        </div>
                    </div>

                    <div class="field">
                        <label class="label has-text-grey-light">Journal Title</label>
                        <div class="control">
                            <input class="input" type="text" name="title" bind:value={formData.title} required style="background-color: #111; color: white; border-color: #444;" />
                        </div>
                    </div>

                    <div class="field">
                        <label class="label has-text-grey-light">Rating</label>
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="rating" bind:value={formData.rating} style="background-color: #111; color: white; border-color: #444;">
                                    <option value="5">⭐⭐⭐⭐⭐</option>
                                    <option value="4">⭐⭐⭐⭐</option>
                                    <option value="3">⭐⭐⭐</option>
                                    <option value="2">⭐⭐</option>
                                    <option value="1">⭐</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div class="field">
                        <label class="label has-text-grey-light">Note / Review</label>
                        <div class="control">
                            <textarea class="textarea" name="note" bind:value={formData.note} required style="background-color: #111; color: white; border-color: #444;"></textarea>
                        </div>
                    </div>

                    <div class="buttons is-right mt-5">
                        <button type="button" class="button is-dark" onclick={closeModal}>Cancel</button>
                        <button type="submit" class="button has-text-weight-bold" style="background-color: #ccff00; color: black;">
                            {isEditMode ? 'Save Changes' : 'Post Review'}
                        </button>
                    </div>
                </form>
            </section>
        </div>
    </div>
{/if}
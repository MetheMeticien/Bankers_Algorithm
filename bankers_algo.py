import streamlit as st
import numpy as np
import pandas as pd

def print_state(step, processes, allocation, need, finish, work):
    st.write(f"### Step {step}:")
    df = pd.DataFrame({
        "Process": processes,
        "Allocation": [list(map(int, alloc)) for alloc in allocation],
        "Need": [list(map(int, n)) for n in need],
        "Finish": finish
    })
    st.write(df)
    st.write(f"**Available (Work):** {list(map(int, work))}")
    st.write("---")

def is_safe_state(processes, available, max_demand, allocation):
    num_processes = len(processes)
    need = max_demand - allocation
    work = available.copy()
    finish = np.zeros(num_processes, dtype=bool)
    safe_sequence = []
    step = 0
    print_state(step, processes, allocation, need, finish, work)

    while len(safe_sequence) < num_processes:
        allocated = False
        for i in range(num_processes):
            if not finish[i] and np.all(need[i].astype(int) <= work.astype(int)):
                work += allocation[i]
                finish[i] = True
                safe_sequence.append(processes[i])
                step += 1
                print_state(step, processes, allocation, need, finish, work)
                allocated = True
                break
        if not allocated:
            st.error("No further allocation possible. System is in an unsafe state!")
            return False, []
    return True, safe_sequence

def get_all_safe_sequences(processes, available, max_demand, allocation):
    need = max_demand - allocation
    work = available.copy()
    finish = np.zeros(len(processes), dtype=bool)
    safe_sequences = []

    def find_safe_sequences(sequence, work, finish):
        allocated = False
        for i in range(len(processes)):
            if not finish[i] and np.all(need[i] <= work):
                new_work = work + allocation[i] 
                new_finish = finish.copy()  
                new_finish[i] = True
                find_safe_sequences(sequence + [processes[i]], new_work, new_finish)
                allocated = True

        if not allocated and all(finish):
            safe_sequences.append(sequence)

    find_safe_sequences([], work, finish)
    return safe_sequences


st.title("Banker's Algorithm Simulator")
uploaded_file = st.file_uploader("Upload a TSV file", type=["tsv", "txt"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, delimiter="\t")
    try:
        processes = df["PID"].astype(str).tolist()
        allocation = df.filter(like="Allocation").astype(int).to_numpy()
        max_demand = df.filter(like="Max").astype(int).to_numpy()
        available = df.filter(like="Available").iloc[0].dropna().astype(int).to_numpy()
        st.success("Valid File Format")
        safe, sequence = is_safe_state(processes, available, max_demand, allocation)
        if safe:
            st.success(f"System is in a safe state. Safe sequence: {sequence}")
            all_sequences = get_all_safe_sequences(processes, available, max_demand, allocation)
            st.write("### All Possible Safe Sequences:")
            for i, seq in enumerate(all_sequences):
                st.write(f"{i+1}: {seq}")
        else:
            st.error("System is in an unsafe state!")
    except Exception as e:
        st.error(f"Invalid file format: {e}")
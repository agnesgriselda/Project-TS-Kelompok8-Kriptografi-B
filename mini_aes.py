import streamlit as st
import csv
import io

S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

def int_to_nibbles(val):
    return [(val >> 12) & 0xF, (val >> 8) & 0xF, (val >> 4) & 0xF, val & 0xF]

def nibbles_to_int(nibs):
    return (nibs[0] << 12) | (nibs[1] << 8) | (nibs[2] << 4) | nibs[3]

def sub_nibbles(state):
    return [S_BOX[n] for n in state]

def shift_rows(state):
    return [state[0], state[1], state[3], state[2]]

def add_round_key(state, round_key):
    return [s ^ k for s, k in zip(state, round_key)]

def mul(a, b):
    p = 0
    for _ in range(4):
        if b & 1:
            p ^= a
        carry = a & 0x8
        a <<= 1
        if carry:
            a ^= 0x13
        a &= 0xF
        b >>= 1
    return p

def mix_columns(state):
    s0, s1, s2, s3 = state
    return [
        mul(1, s0) ^ mul(4, s2),
        mul(1, s1) ^ mul(4, s3),
        mul(4, s0) ^ mul(1, s2),
        mul(4, s1) ^ mul(1, s3)
    ]

def key_expansion(key):
    k = int_to_nibbles(key)
    w = [0]*6
    w[0], w[1] = k[0:2]
    w[2] = w[0] ^ S_BOX[w[1]]
    w[3] = w[2] ^ w[1]
    w[4] = w[2] ^ S_BOX[w[3]]
    w[5] = w[4] ^ w[3]
    return [
        [w[0], w[1], w[0], w[1]],
        [w[2], w[3], w[2], w[3]],
        [w[4], w[5], w[4], w[5]],
        [w[4], w[5], w[4], w[5]]
    ]

def mini_aes_encrypt(plain_int, key_int):
    logs = []
    state = int_to_nibbles(plain_int)
    round_keys = key_expansion(key_int)

    logs.append(f"Initial State: {state}")

    state = add_round_key(state, round_keys[0])
    logs.append(f"After Round 0 (AddRoundKey): {state}")

    state = sub_nibbles(state)
    logs.append(f"After SubNibbles R1: {state}")
    state = shift_rows(state)
    logs.append(f"After ShiftRows R1: {state}")
    state = mix_columns(state)
    logs.append(f"After MixColumns R1: {state}")
    state = add_round_key(state, round_keys[1])
    logs.append(f"After AddRoundKey R1: {state}")

    state = sub_nibbles(state)
    logs.append(f"After SubNibbles R2: {state}")
    state = shift_rows(state)
    logs.append(f"After ShiftRows R2: {state}")
    state = mix_columns(state)
    logs.append(f"After MixColumns R2: {state}")
    state = add_round_key(state, round_keys[2])
    logs.append(f"After AddRoundKey R2: {state}")

    state = sub_nibbles(state)
    logs.append(f"After SubNibbles R3: {state}")
    state = shift_rows(state)
    logs.append(f"After ShiftRows R3: {state}")
    state = add_round_key(state, round_keys[3])
    logs.append(f"After AddRoundKey R3: {state}")

    ciphertext = nibbles_to_int(state)
    logs.append(f"Final Ciphertext (Hex): {hex(ciphertext)}")

    return ciphertext, logs

def mini_aes_ecb_encrypt(plaintext_blocks, key_int):
    ciphertext_blocks = []
    all_logs = []
    for idx, block in enumerate(plaintext_blocks):
        ciphertext, logs = mini_aes_encrypt(block, key_int)
        ciphertext_blocks.append(ciphertext)
        all_logs.append((idx, logs))
    return ciphertext_blocks, all_logs

def mini_aes_cbc_encrypt(plaintext_blocks, key_int, iv):
    ciphertext_blocks = []
    all_logs = []
    previous = iv
    for idx, block in enumerate(plaintext_blocks):
        block ^= previous
        ciphertext, logs = mini_aes_encrypt(block, key_int)
        ciphertext_blocks.append(ciphertext)
        all_logs.append((idx, logs))
        previous = ciphertext
    return ciphertext_blocks, all_logs

def generate_txt(plaintext, key, ciphertext, logs):
    output = io.StringIO()
    output.write(f"Plaintext: {bin(plaintext)[2:].zfill(16)}\n")
    output.write(f"Key: {bin(key)[2:].zfill(16)}\n")
    output.write(f"Ciphertext: {hex(ciphertext)}\n")
    output.write("Logs:\n")
    for log in logs:
        output.write(log + "\n")
    return output.getvalue()

def generate_txt_blocks(plaintexts, key, ciphertexts, logs_per_block):
    output = io.StringIO()
    for i, (pt, ct, logs) in enumerate(zip(plaintexts, ciphertexts, logs_per_block)):
        output.write(f"Block {i+1}:\n")
        output.write(f"Plaintext: {bin(pt)[2:].zfill(16)}\n")
        output.write(f"Key: {bin(key)[2:].zfill(16)}\n")
        output.write(f"Ciphertext: {hex(ct)}\n")
        output.write("Logs:\n")
        for log in logs:
            output.write(log + "\n")
        output.write("\n")
    return output.getvalue()

def generate_csv(plaintext, key, ciphertext, logs):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Plaintext', 'Key', 'Ciphertext'])
    writer.writerow([bin(plaintext)[2:].zfill(16), bin(key)[2:].zfill(16), hex(ciphertext)])
    writer.writerow(['Logs'])
    for log in logs:
        writer.writerow([log])
    return output.getvalue()

def generate_csv_blocks(plaintexts, key, ciphertexts, logs_per_block):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Block', 'Plaintext', 'Key', 'Ciphertext'])
    for i, (pt, ct) in enumerate(zip(plaintexts, ciphertexts)):
        writer.writerow([f'Block {i+1}', bin(pt)[2:].zfill(16), bin(key)[2:].zfill(16), hex(ct)])
        writer.writerow(['Logs'])
        for log in logs_per_block[i]:
            writer.writerow([log])
    return output.getvalue()

def load_from_txt(filename):
    with open(filename, 'r') as f:
        return f.read()

def load_from_csv(filename):
    with open(filename, 'r') as f:
        return f.read()

# --- STREAMLIT GUI ---
st.title("Mini-AES 16-bit Encryption")

mode = st.selectbox("Select Encryption Mode:", ("Single Block", "ECB", "CBC"))
plaintext_input = st.text_input("Enter Plaintext (binary, multiples of 16 bits, e.g., 1101011100101000):")
key_input = st.text_input("Enter Key (16-bit binary, e.g., 0100101011110101):")
iv_input = ""
if mode == "CBC":
    iv_input = st.text_input("Enter IV (16-bit binary for CBC mode):")

output_ciphertexts = []
output_logs = []
output_plaintext = None
output_key = None

if st.button("Encrypt"):
    try:
        if len(key_input) != 16:
            st.error("Key must be exactly 16 bits long!")
        elif mode == "CBC" and len(iv_input) != 16:
            st.error("IV must be exactly 16 bits long!")
        else:
            key = int(key_input, 2)
            plaintext_blocks = [int(plaintext_input[i:i+16], 2) for i in range(0, len(plaintext_input), 16)]
            output_plaintext = plaintext_blocks[0] if len(plaintext_blocks) == 1 else 0
            output_key = key

            if mode == "Single Block":
                if len(plaintext_blocks) != 1:
                    st.error("Single Block mode requires exactly one 16-bit block!")
                else:
                    ciphertext, logs = mini_aes_encrypt(plaintext_blocks[0], key)
                    output_ciphertexts = [ciphertext]
                    output_logs = logs
                    st.success(f"Ciphertext (hex): {hex(ciphertext)}")
                    st.subheader("Encryption Steps:")
                    for log in logs:
                        st.text(log)
            elif mode == "ECB":
                ciphertext_blocks, all_logs = mini_aes_ecb_encrypt(plaintext_blocks, key)
                output_ciphertexts = ciphertext_blocks
                output_logs = [logs for _, logs in all_logs]
                st.success(f"Ciphertext Blocks (hex): {[hex(c) for c in ciphertext_blocks]}")
                for idx, logs in all_logs:
                    st.subheader(f"Block {idx+1} Encryption Steps:")
                    for log in logs:
                        st.text(log)
            elif mode == "CBC":
                iv = int(iv_input, 2)
                ciphertext_blocks, all_logs = mini_aes_cbc_encrypt(plaintext_blocks, key, iv)
                output_ciphertexts = ciphertext_blocks
                output_logs = [logs for _, logs in all_logs]
                st.success(f"Ciphertext Blocks (hex): {[hex(c) for c in ciphertext_blocks]}")
                for idx, logs in all_logs:
                    st.subheader(f"Block {idx+1} Encryption Steps:")
                    for log in logs:
                        st.text(log)
    except Exception as e:
        st.error(f"Error: {e}")

if output_ciphertexts:
    st.subheader("Download the Result")
    if mode == "Single Block":
        txt_data = generate_txt(output_plaintext or 0, output_key or 0, output_ciphertexts[0], output_logs)
        csv_data = generate_csv(output_plaintext or 0, output_key or 0, output_ciphertexts[0], output_logs)
    else:
        txt_data = generate_txt_blocks(plaintext_blocks, output_key, output_ciphertexts, output_logs)
        csv_data = generate_csv_blocks(plaintext_blocks, output_key, output_ciphertexts, output_logs)

    st.download_button(
        label="Download TXT File",
        data=txt_data,
        file_name="mini_aes_result.txt",
        mime="text/plain"
    )

    st.download_button(
        label="Download CSV File",
        data=csv_data,
        file_name="mini_aes_result.csv",
        mime="text/csv"
    )

st.subheader("Load Existing Result")
load_filename = st.text_input("Filename to Load:", value="result.txt")
if st.button("Load from TXT"):
    content = load_from_txt(load_filename)
    st.code(content)
if st.button("Load from CSV"):
    content = load_from_csv(load_filename)
    st.code(content)
with open("6.txt", "r", newline="\n") as f:
	signal = f.read()

def locate_marker(length:int) -> int:
	for i in range(len(signal) - length):
		if len(set(signal[i:i + length])) == length:
			marker_end = i + length
			break

	else: #nobreak
		marker_end = "No marker found"

	return marker_end

packet_start = locate_marker(4)
message_start = locate_marker(14)
print(packet_start, message_start)

from TCP_socket_p2 import TCP_Connection
from header_maker import *
from TCP_socket_p2 import *

class TCP_Connection_Final(TCP_Connection):
	"""docstring for TCP_Connection_Final"""
	def __init__(self, self_address, dst_address, self_seq_num, dst_seq_num, log_file=None):
		super().__init__(self_address, dst_address, self_seq_num, dst_seq_num, log_file)
	def handle_timeout(self):
		#put code to handle RTO timeout here
		#send a single packet containing the oldest unacknowledged data
		#increase the RTO timer 

		#Check the RTO timer and if it has expired, resend the oldest unack packet.
		#IF there's a timeout regarding the zero window probe, handle it as per the instructions

		#If rto timer has gone off.
		if self.RTO_timer.time_up():
		# Assuming we have a method or mechanism to get the oldest unacknowledged packet
			oldest_unacked_packet = self.get_oldest_unacknowledged_packet()
		
		# Load the oldest unacknowledged packet into the send_buff
		if len(self.send_buff) + len(oldest_unacked_packet) <= SEND_BUFF_SIZE:
			for datum in oldest_unacked_packet: 
				self.send_buff.append(datum)

			# Drain the send buffer, i.e., resend the packet
			while self.send_buff:
				self._main_loop()
				
		# Reset and update the RTO timer using check_time method
		self.RTO_timer.reset_timer()
		self.RTO_timer.check_time()  # Assuming this method updates and starts the timer with the new value

		# Logic for zero window probing (if required) can be added here









		pass
	def handle_window_timeout(self):
		#put code to handle window timeout here
		#in other words, if we haven't sent any data in while (which causes this time to go off),
		#send an empty packet

		#Handle the zero window probing specifically






		pass
	def receive_packets(self, packets):
		#insert code to deal with a list of incoming packets here
		#NOTE: this code can send one packet, but should never send more than one packet

		# For each packet:
		# Validate the seq number
		# Trim any bytes that lie outside the window
		# Check the ACK field and update SND.UNA and SND.WND accordingly
		# Process the segment text.
		# If PUSH flag is set, mark the corresponding byte
		# Send an ack if the packet contains new data

		for packet in packets:
			# Assuming header_maker provides the functionality to parse the header
			seq_num, ack_num, flags, window_size, data = header_maker.parse_header(packet)

			# Check if the segment is within the expected window (embedded logic)
			if not (self.RCV.NXT <= seq_num < self.RCV.NXT + self.RCV.WND):
				continue

			# Place data in the correct location in the receive buffer
			offset = seq_num - self.RCV.NXT
			self.receive_buffer[offset:offset + len(data)] = data

			# Handle the PSH flag (simple logic)
			if flags & PSH:
				# Handle the PSH flag by marking the data, this might need further refinement
				data = data + b'PSH'

			# Update RTT and RTO timers using available timer methods (Assumption)
			if self.RTT_timer.check_time():
				self.RTT_timer.set_and_start(seq_num)
			if self.RTO_timer.check_time():
				self.RTO_timer.set_and_start(ack_num)

			# Adjust the receive window
			self.RCV.WND = window_size

			# Send an acknowledgment for the received data (using the send method)
			self.send(b'', ack_num=self.RCV.NXT, flags=ACK)


	def send_data(self, window_timeout = False, RTO_timeout = False):
		#put code to send a single packet of data here
		#note that this code does not always need to send data, only if TCP policy thinks it makes sense
		#if there is any data to send, i.e. we have data we have not sent and we are allowed to send by our
		#congestion and flow control windows, then send one packet of that data

		# Determine the max size of the data packet to be sent based on SND.MSS, and SND.WND
		# and self.congestion.window
		# Send the data using "_packetize_and_send"
		# Update timers as required
		# IF PSH is set in the data, mark the corresponding byte
		# Handle zero window probing as needed






		pass

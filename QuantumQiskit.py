import qiskit
#
qiskit.__qiskit_version__
#
from qiskit import IBMQ
#
from qiskit import *
from qiskit.tools.visualization import plot_histogram
%matplotlib inline
#
circuit2 = QuantumCircuit(2, 2)
circuit2.h(0)
circuit2.h(1)
circuit2.barrier()
circuit2.x(0)
circuit2.cz(0,1)
circuit2.x(0)
circuit2.barrier()
circuit2.h(0)
circuit2.h(1)
circuit2.x(0)
circuit2.x(1)
circuit2.cz(0,1)
circuit2.x(0)
circuit2.x(1)
circuit2.h(0)
circuit2.h(1)
circuit2.barrier()
circuit2.measure([0,1], [0,1])

backend = Aer.get_backend('qasm_simulator')
results = execute(circuit2, backend=backend, shots=1024).result()
answer = results.get_counts()
plot_histogram(answer)
circuit2.draw(output='mpl')
#
circuit3 = QuantumCircuit(3, 3)
circuit3.h(0)
circuit3.h(1)
circuit3.h(2)
circuit3.barrier()
circuit3.x(1)
circuit3.h(2)
circuit3.ccx(0,1,2)
circuit3.x(1)
circuit3.h(2)
circuit3.barrier()
circuit3.h(0)
circuit3.h(1)
circuit3.h(2)
circuit3.x(0)
circuit3.x(1)
circuit3.x(2)
circuit3.h(2)
circuit3.ccx(0,1,2)
circuit3.h(2)
circuit3.x(0)
circuit3.x(1)
circuit3.x(2)
circuit3.h(0)
circuit3.h(1)
circuit3.h(2)
circuit3.barrier()
circuit3.measure([0,1,2], [0,1,2])

backend = Aer.get_backend('qasm_simulator')
results = execute(circuit3, backend=backend, shots=1024).result()
answer = results.get_counts()
plot_histogram(answer)
circuit3.draw(output='mpl')
#
provider = IBMQ.get_provider('ibm-q')
qcomp = provider.get_backend('ibmq_athens')
job = execute(circuit2, backend=qcomp)
from qiskit.tools.monitor import job_monitor
job_monitor(job)
#
result = job.result()
plot_histogram(result.get_counts(circuit2))
#
job2 = execute(circuit3, backend=qcomp)
job_monitor(job2)
#
result2 = job2.result()
plot_histogram(result2.get_counts(circuit3))
#
#Mitigation grover 2
from qiskit.ignis.mitigation.measurement import (complete_meas_cal, CompleteMeasFitter)
cal_circuits, state_labels = complete_meas_cal(qr = circuit2.qregs[0], circlabel = 'measerrormitigationcal')
cal_circuits[2].draw(output='mpl')
#
cal_job = execute(cal_circuits, backend = qcomp, shots = 1024, optimization_level = 0)
print(cal_job.job_id())
job_monitor(cal_job)
cal_results = cal_job.result()
#
plot_histogram(cal_results.get_counts(cal_circuits[3]))
#
meas_fitter = CompleteMeasFitter(cal_results, state_labels)
meas_fitter.plot_calibration()
#
meas_filter = meas_fitter.filter
mitigated_result = meas_filter.apply(result)
device_counts = result.get_counts(circuit2)
mitigated_counts = mitigated_result.get_counts(circuit2)
plot_histogram([device_counts, mitigated_counts], legend=['device, noisy', 'device, mitigated'])
#
#Mitigation grover 3
cal_circuits2, state_labels2 = complete_meas_cal(qr = circuit3.qregs[0], circlabel = 'measerrormitigationcal')
cal_circuits2[2].draw(output='mpl')
#
cal_job2 = execute(cal_circuits2, backend = qcomp, shots = 1024, optimization_level = 0)
print(cal_job2.job_id())
job_monitor(cal_job2)
cal_results2 = cal_job2.result()
#
plot_histogram(cal_results2.get_counts(cal_circuits2[7]))
#
meas_fitter2 = CompleteMeasFitter(cal_results2, state_labels2)
meas_fitter2.plot_calibration()
#
meas_filter2 = meas_fitter2.filter
mitigated_result2 = meas_filter2.apply(result2)
device_counts2 = result2.get_counts(circuit3)
mitigated_counts2 = mitigated_result2.get_counts(circuit3)
plot_histogram([device_counts2, mitigated_counts2], legend=['device, noisy', 'device, mitigated'])
#
circuit4 = QuantumCircuit(2,2)
circuit4.cz(0,1)

circuit4.measure_all()


backend = Aer.get_backend('qasm_simulator')
results = execute(circuit4, backend=backend, shots=1024).result()
answer = results.get_counts()
plot_histogram(answer)
#circuit4.draw(output='mpl')
#
circuit5 = QuantumCircuit(2,2)
circuit5.h(1)
circuit5.cx(0,1)
circuit5.h(1)

circuit5.measure_all()


backend = Aer.get_backend('qasm_simulator')
results = execute(circuit5, backend=backend, shots=1024).result()
answer = results.get_counts()
plot_histogram(answer)
#circuit5.draw(output='mpl')
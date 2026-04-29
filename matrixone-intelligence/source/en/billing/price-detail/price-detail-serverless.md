# Pricing: Serverless production instances

## CU

A Compute Unit (CU) is the basic unit of compute for a MatrixOne Intelligence Serverless instance. Every SQL query consumes a certain number of CUs, covering CPU, memory, object-storage I/O, and public network egress.

We define 1 CU = the compute consumed when MatrixOne reads 32 KB of data. The mapping from resource consumption to CU count:

<table>
  <tr>
    <th>Resource</th>
    <th>Usage</th>
    <th>CUs consumed</th>
  </tr>
  <tr>
    <td >CPU</td>
    <td>1 ms*core</td>
    <td>0.052</td>
  </tr>
  <tr>
    <td >Memory</td>
    <td>1 GB*s </td>
    <td>10.9 </td>
  </tr>
  <tr>
    <td >Network (public)</td>
    <td>1 KB Network egress</td>
    <td> 0.74</td>
  </tr>
  <tr>
    <td> Network (private)</td>
    <td>1 KB Network egress</td>
    <td>0</td>
  </tr>
  <tr>
    <td rowspan="2" style="vertical-align: middle;">Storage I/O</td>
    <td>1 storage read request </td>
    <td> 0.97 </td>
  </tr>
  <tr>
    <td>1 storage write request</td>
    <td>0.97</td>
  </tr>
</table>

MO Intelligence currently prices CUs at **¥1 per 100,000 CUs**.

## Storage

Storage is the size of the data you store in a MatrixOne Intelligence instance. MO Intelligence prices storage at **¥0.15/GiB-month**.

# Deployment FAQ

## Environment

**What operating system versions does MatrixOne require?**

- The following Linux distributions are supported:

| Linux OS                 | Version                |
| :----------------------- | :--------------------- |
| Debian                   | 11.0 or later          |
| Ubuntu LTS               | 20.04 or later         |
| Red Hat Enterprise Linux | 9.0 or later releases  |
| Oracle Enterprise Linux  | 9.0 or later releases  |
| CentOS                   | 7.0 or later releases  |

For Linux distributions with older kernels, we recommend using the musl-libc-based binary when installing from a binary package — see the "Recommended install environment" section of [Standalone MatrixOne installation overview](../Get-Started/install-standalone-matrixone.md).

- macOS is supported, but only recommended for testing and development:

| macOS | Version                |
| :---- | :--------------------- |
| macOS | Monterey 12.3 or later |

- As a Chinese-developed database, MatrixOne is also compatible with the following domestic operating systems:

| OS | Version | CPU | Memory |
| :--- | :--- | :--- | :--- |
| OpenCloudOS | v8.0 / v9.0 | x86 CPU; 4 cores | 16 GB |
| openEuler | 20.03 | x86 / ARM CPU; 4 cores | 16 GB |
| TencentOS Server | v2.4 / v3.1 | x86 CPU; 4 cores | 16 GB |
| UnionTech (Uniontech) | V20 | ARM CPU; 4 cores | 16 GB |
| Kylin | V10 | ARM CPU; 4 cores | 16 GB |
| Kylinsec | v3.4 | x86 / ARM CPU; 4 cores | 16 GB |

**Can MatrixOne run on Red Hat family distros like CentOS 7?**

MatrixOne has loose OS requirements and does run on CentOS 7, but CentOS 7 reached end-of-life at the end of June 2024 — we recommend a more recent OS.

**Does MatrixOne support deployment in domestic (Chinese) environments?**

For domestic CPUs and OSes: MatrixOne has been adapted for Kunpeng and Hygon CPUs, and for Kylin, openEuler, and Kylinsec operating systems.

**Where can MatrixOne be deployed?**

Anywhere: on-premises, public cloud, private cloud, or Kubernetes.

**Can MatrixOne be deployed in a distributed topology on Alibaba Cloud ECS?**

Yes — you'll need to build Kubernetes on top of ECS, or use Alibaba Cloud ACK.

**Is distributed deployment only supported on Kubernetes? Can I do physical distributed deployments locally?**

If you don't have an existing Kubernetes + MinIO environment, our installer ships Kubernetes and MinIO bundled — you can do a one-command deployment on bare metal.

* **Does the non-Kubernetes version support primary-standby configurations?**

Not yet — support is planned.

**Is production deployment Kubernetes-only?**

Yes — for distributed stability and scalability, we recommend Kubernetes in production. If you don't have Kubernetes, use a managed Kubernetes service to reduce complexity.

## Hardware

**What are the hardware requirements for deploying MatrixOne?**

Standalone deployments run on Intel x86-64 or ARM 64-bit commodity servers.

Dev / test / production server recommendations:

- Development / test

| CPU | Memory | Local storage |
| :--- | :--- | :--- |
| 4 core+ | 16 GB+ | SSD/HDD 200 GB+ |

ARM-based MacBook M1 / M2 is also suitable for development.

- Production

| CPU | Memory | Local storage |
| :--- | :--- | :--- |
| 16 core+ | 64 GB+ | SSD/HDD 500 GB+ |

For distributed deployments, see [Cluster topology planning](../Deploy/deployment-topology/topology-overview.md).

## Configuration

**Do I need to change any settings during installation?**

In most cases no — the default `launch.toml` works out of the box. If you want to customize listening ports, IP address, or data-file paths, edit the corresponding [`cn.toml`](https://github.com/matrixorigin/matrixone/blob/main/etc/launch-with-proxy/cn.toml), [`tn.toml`](https://github.com/matrixorigin/matrixone/blob/main/etc/launch-with-proxy/tn.toml), or [`log.toml`](https://github.com/matrixorigin/matrixone/blob/main/etc/launch-with-proxy/log.toml) — see [Common parameter configuration](../Reference/System-Parameters/system-parameter.md).

**How do I place MatrixOne's data directory in a specific path?**

With Docker, mount your path into the container — see [Mount a directory into a Docker container](../Maintain/mount-data-by-docker.md).

If you build and run from source or binary, edit `matrixone/etc/launch-with-proxy/` — in `cn.toml`, `tn.toml`, and `log.toml`, change `data-dir = "./mo-data"` to `data-dir = "your_local_path"`, save, and restart.

## Tools

**Can binary-package installs be managed with `mo_ctl`?**

Yes — set `MO_PATH` to the binary path and you can use `mo_ctl`.

**Does `mo_ctl` support source-build upgrades?**

Yes — the `upgrade` command lets you specify a version or commit ID for fine-grained upgrades. You'll need to set the current `MO_PATH` and have a working compile environment.

**Does `mo_ctl` support deploying MatrixOne clusters?**

Not yet — cluster deployment and management will be added later.

**After installing the operator via Helm, how do I verify the install succeeded?**

Run `helm list -A`.

**How do I uninstall a Helm-installed operator?**

Use `helm uninstall` with the release name and namespace.

**Does the operator version need to match the cluster version?**

The operator manages the MatrixOne cluster, so keep its version close to the cluster version — e.g., for a 1.0.0-rc2 cluster, pre-install the 1.0.0-rc2 operator. If an exact match isn't available, pick the nearest version.

## Errors

**After installing the MySQL client, running `mysql` returns `command not found: mysql`. How do I fix it?**

The PATH isn't set. Open a new terminal and run:

::::{tab-set}

:::{tab-item} Linux

```bash
echo 'export PATH="/path/to/mysql/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

Replace `/path/to/mysql/bin` with your MySQL install path — typically `/usr/local/mysql/bin`. If you're not sure, find it via:

```bash
whereis mysql
```
:::

:::{tab-item} macOS

macOS 10 and later use `zsh` as default shell — example below. If you use a different shell, adjust accordingly.

```zsh
echo export PATH=/path/to/mysql/bin:$PATH >> ~/.zshrc
source ~/.zshrc
```

Replace `/path/to/mysql/bin` with your MySQL install path — typically `/usr/local/mysql/bin`. If you're not sure, find it via:

```bash
whereis mysql
```
:::

::::

**When building MatrixOne from source, I see errors or build failures — how do I proceed?**

Error: `Get "https://proxy.golang.org/........": dial tcp 142.251.43.17:443: i/o timeout`

MatrixOne builds depend on many Go libraries, which are downloaded at build time. The above error is a download timeout — it's a network issue.

- If you're on a mainland-China network, point your Go module proxy at a Chinese mirror to speed up downloads.

- Check your Go env with `go env`. If you see `GOPROXY="https://proxy.golang.org,direct"`, switch it:

```
go env -w GOPROXY=https://goproxy.cn,direct
```

After that, `make build` should complete quickly.

**When testing MatrixOne with MO-Tester, I get `too many open files` — how do I fix it?**

MO-Tester rapidly opens and closes many SQL files, quickly hitting the default per-process file limit on Linux / macOS. That's the cause.

* macOS: raise the limit in one command:

```
ulimit -n 65536
```

* Linux: follow a detailed [guide](https://www.linuxtechi.com/set-ulimit-file-descriptors-limit-linux-servers/) to set `ulimit` to 100000.

Afterwards the error should go away.

**On an M1 Mac, `ssb-dbgen` fails to compile during SSB testing**

On M1 hardware you need a couple of extra steps before building `ssb-dbgen`:

1. Download and install [GCC 11](https://gcc.gnu.org/install/).

2. Confirm `gcc-11` is installed:

    ```
    gcc-11 -v
    ```

    A successful install looks like:

    ```
    Using built-in specs.
    COLLECT_GCC=gcc-11
    COLLECT_LTO_WRAPPER=/opt/homebrew/Cellar/gcc@11/11.3.0/bin/../libexec/gcc/aarch64-apple-darwin21/11/lto-wrapper
    Target: aarch64-apple-darwin21
    Configured with: ../configure --prefix=/opt/homebrew/opt/gcc@11 --libdir=/opt/homebrew/opt/gcc@11/lib/gcc/11 --disable-nls --enable-checking=release --with-gcc-major-version-only --enable-languages=c,c++,objc,obj-c++,fortran --program-suffix=-11 --with-gmp=/opt/homebrew/opt/gmp --with-mpfr=/opt/homebrew/opt/mpfr --with-mpc=/opt/homebrew/opt/libmpc --with-isl=/opt/homebrew/opt/isl --with-zstd=/opt/homebrew/opt/zstd --with-pkgversion='Homebrew GCC 11.3.0' --with-bugurl=https://github.com/Homebrew/homebrew-core/issues --build=aarch64-apple-darwin21 --with-system-zlib --with-sysroot=/Library/Developer/CommandLineTools/SDKs/MacOSX12.sdk
    Thread model: posix
    Supported LTO compression algorithms: zlib zstd
    gcc version 11.3.0 (Homebrew GCC 11.3.0)
    ```

3. Edit `bm_utils.c` under the `ssb-dbgen` directory:

    - Line 41: change `#include <malloc.h>` → `#include <sys/malloc.h>`
    - Line 398: change `open(fullpath, ((*mode == 'r')?O_RDONLY:O_WRONLY)|O_CREAT|O_LARGEFILE,0644);` → `open(fullpath, ((*mode == 'r')?O_RDONLY:O_WRONLY)|O_CREAT,0644);`

4. Edit `varsub.c` under the `ssb-dbgen` directory:

    - Line 5: change `#include <malloc.h>` → `#include <sys/malloc.h>`

5. Edit the `makefile` under the `ssb-dbgen` directory:

    - Line 5: change `CC = gcc` → `CC = gcc-11`

6. Go back into `ssb-dbgen` and build:

    ```
    cd ssb-dbgen
    make
    ```

7. If a `dbgen` executable appears in the `ssb-dbgen` directory, the build succeeded.

**After building MatrixOne from the `main` branch, switching to another version and rebuilding panics.**

This can happen when switching to a version earlier than 0.8.0 and using `make build`. It's a storage-format incompatibility that existed before 0.8.0; from 0.8.0 onward compatibility is maintained.

:::{note}
In this case we strongly recommend reinstalling the latest stable MatrixOne version for continued data compatibility. We also recommend `mo_ctl` for quick build and start.
:::

Specifically, before 0.8.0, `make build` auto-generated a data directory named *mo-data*. If you switched branches and ran `make build` again, the system didn't auto-delete *mo-data*, and the format mismatch caused panic.

Workaround: clean *mo-data* first (`rm -rf mo-data`), then rebuild.

Example using the older build flow:

```
[root ~]# cd matrixone            // enter the matrixone directory
[root ~]# git branch              // check current branch
* 0.8.0
[root ~]# make build              // build matrixone
...                               // build output elided. Then switch to another version, e.g. 0.7.0:
[root ~]# git checkout 0.7.0      // switch to 0.7.0
[root ~]# rm -rf mo-data          // clean the data directory
[root ~]# make build              // rebuild matrixone
...                               // build output elided
```

**I'm using a CN tag to connect to proxy and get a password-verification error when logging into the MatrixOne cluster.**

- **Cause**: connection-string format error. When connecting via MySQL client, MatrixOne extends the username field — append `?` after the username, followed by CN-group tags. Tag key-value pairs are separated by `=`; multiple pairs are comma-separated.

- **Fix**: see the examples below.

Suppose your `mo.yaml` has the following CN-group config:

```yaml
## only the relevant portion
...
- cacheVolume:
    size: 100Gi
  cnLabels:
  - key: workload
    values:
    - bk
...
```

To connect with the MySQL client, use: `mysql -u root?workload=bk -p111 -h 10.206.16.10 -P 31429`. Here `workload=bk` is the CN tag, joined with `=`.

**After installing the latest operator, a pod named `job-bucket` never comes up — how do I debug?**

Check whether the MinIO secret is missing — it might be that MinIO connection info isn't configured and the pod can't reach MinIO.

Similarly, when exporting with `mo-dump`, an example command is: `mo-dump -u "dump?workload=bk" -h 10.206.16.10 -P 31429 -db tpch_10g > /tmp/mo/tpch_10g.sql`.

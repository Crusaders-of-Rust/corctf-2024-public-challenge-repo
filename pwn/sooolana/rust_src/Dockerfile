FROM ubuntu:24.04 AS builder

RUN apt-get update && apt-get install cargo rustc git -y
RUN git clone https://github.com/solana-labs/rbpf.git /rbpf
WORKDIR /rbpf
RUN git reset --hard f3758ecee89198433422f751beee7f0f52dbcd55
RUN sed 's/instruction_end.sub(4)/instruction_end.sub(5)/g' -i src/jit.rs
COPY . challenge/
RUN cd challenge/ && cargo build --release

FROM scratch AS export
COPY --from=builder /rbpf/challenge/target/release/challenge /challenge

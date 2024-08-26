use std::fs::read_to_string;
use std::io;
use std::sync::Arc;

use solana_rbpf::ebpf;
use solana_rbpf::ebpf::MM_STACK_START;
use solana_rbpf::memory_region::{MemoryMapping, MemoryRegion};
use solana_rbpf::program::{BuiltinProgram, SBPFVersion};
use solana_rbpf::verifier::RequisiteVerifier;
use solana_rbpf::vm::{Config, EbpfVm, TestContextObject};

fn main() {
	unsafe {
		let config = Config { enable_sbpf_v1: true,
		                      enable_sbpf_v2: true,
		                      noop_instruction_rate: 0,
		                      instruction_meter_checkpoint_distance: 100000,
		                      enable_symbol_and_section_labels: true,
		                      ..Default::default() };

		let loader =
			Arc::new(BuiltinProgram::<TestContextObject>::new_loader(config, Default::default()));
        let src = io::read_to_string(io::stdin()).unwrap();
		let mut application = solana_rbpf::assembler::assemble(&src, loader.clone()).unwrap();
		application.verify::<RequisiteVerifier>().unwrap();
		application.jit_compile().unwrap();
        println!("Compiled");

		let mut ctx = TestContextObject::new(100000);
		let mut stack = [0u8; 1024];
		let memory = MemoryMapping::new(
		                                vec![
			MemoryRegion::new_readonly(&[0u8; 4096], ebpf::MM_PROGRAM_START),
			MemoryRegion::new_writable(&mut stack, MM_STACK_START),
		],
		                                &config,
		                                &SBPFVersion::V3,
		).unwrap();
		let mut vm = EbpfVm::new(loader.clone(), &SBPFVersion::V3, &mut ctx, memory, 1024);

		vm.execute_program(&application, false);
	}
}

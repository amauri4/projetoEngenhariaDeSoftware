"use client";
import { Treino } from "@/app/types/treino";
import { useMemo, useState } from "react";
import { TreinoDetailsModal } from "@/app/components/treino_details";

interface Props {
  treinos: Treino[];
}

export default function InstrutorTreinoList({ treinos }: Props) {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedTreino, setSelectedTreino] = useState<Treino | null>(null);

    const treinosAgrupadosPorAluno = useMemo(() => {
        const treinosAgrupados: Record<string, Treino[]> = {};

        for (const treino of treinos) {
            const responsavelNome = treino.responsavel_nome || "Aluno Não Atribuído";
            if (!treinosAgrupados[responsavelNome]) {
                treinosAgrupados[responsavelNome] = [];
            }
            treinosAgrupados[responsavelNome].push(treino);
        }
        return treinosAgrupados;
    }, [treinos]); 

    const openModal = (treino: Treino) => {
        setSelectedTreino(treino);
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setSelectedTreino(null);
    };

    if (treinos.length === 0) {
        return <p className="text-sm text-gray-500">Nenhum treino criado ainda.</p>;
    }

    return (
        <>
            <div className="space-y-6 mt-6">
                {Object.entries(treinosAgrupadosPorAluno).map(([alunoNome, treinosDoAluno]) => (
                    <div key={alunoNome}>
                        <h3 className="font-bold text-lg text-gray-700 border-b pb-2 mb-3">{alunoNome}</h3>
                        <ul className="space-y-3">
                            {treinosDoAluno.map((treino) => (
                                <li 
                                    key={treino.id} 
                                    className="bg-gray-100 p-4 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer list-none"
                                    onClick={() => openModal(treino)}
                                >
                                    <p className="font-medium text-gray-800">{treino.descricao}</p>
                                    <div className="text-sm text-gray-500 mt-1 flex justify-between">
                                        <span>Início: <strong>{treino.data_inicio ? new Date(`${treino.data_inicio}T00:00:00`).toLocaleDateString()  : 'N/A'}</strong></span>
                                        <span>Entrega: <strong>{treino.data_entrega ? new Date(`${treino.data_entrega}T00:00:00`).toLocaleDateString()  : 'Não definido'}</strong></span>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
            <TreinoDetailsModal
                isOpen={isModalOpen}
                onClose={closeModal}
                treino={selectedTreino}
                userType="instrutor"
            />
        </>
    );
}

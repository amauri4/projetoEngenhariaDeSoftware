"use client";
import { Treino } from "@/app/types/treino";
import { useMemo, useState } from "react";
import { TreinoDetailsModal } from "@/app/components/treino_details";
import { isAfter, isBefore, parseISO } from "date-fns";

interface Props {
  treinos: Treino[];
}

export default function InstrutorTreinoList({ treinos }: Props) {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedTreino, setSelectedTreino] = useState<Treino | null>(null);

    const treinosAtuaisPorAluno = useMemo(() => {
        const hoje = new Date();
        const treinosAgrupados: Record<string, Treino[]> = {};

        for (const treino of treinos) {
            const responsavelId = treino.responsavel_id.toString();
            if (!treinosAgrupados[responsavelId]) {
                treinosAgrupados[responsavelId] = [];
            }
            treinosAgrupados[responsavelId].push(treino);
        }

        const treinosAtuais: Treino[] = [];
        for (const alunoId in treinosAgrupados) {
            const treinoVigente = treinosAgrupados[alunoId].find(t => {
                const inicio = parseISO(`${t.data_inicio}T00:00:00`);
                const fim = t.data_entrega ? parseISO(`${t.data_entrega}T00:00:00`) : null;
                return isAfter(hoje, inicio) && (fim ? isBefore(hoje, fim) : true);
            });
            if (treinoVigente) {
                treinosAtuais.push(treinoVigente);
            }
        }
        return treinosAtuais;
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
            <div className="space-y-3 mt-6">
                {treinosAtuaisPorAluno.map((treino) => (
                    <li 
                        key={treino.id} 
                        className="bg-gray-100 p-4 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer list-none"
                        onClick={() => openModal(treino)}
                    >
                        <p className="font-medium text-gray-800">{treino.descricao}</p>
                        <div className="text-sm text-gray-500 mt-1 flex justify-between">
                            <span>Aluno: <strong>{treino.responsavel_nome || "N/A"}</strong></span>
                            <span>Entrega: <strong>{treino.data_entrega ? new Date(`${treino.data_entrega}T00:00:00`).toLocaleDateString()  : 'Não definido'}</strong></span>
                        </div>
                    </li>
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